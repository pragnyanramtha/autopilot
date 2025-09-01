import { GoogleGenerativeAI } from '@google/generative-ai';
import { CommandParser } from '../parser/CommandParser.js';
import { TaskPlanner } from '../planner/TaskPlanner.js';
import { StatusIndicator } from '../ui/components/StatusIndicator.js';
import { CommandInput, ExecutionMode } from '../types/interfaces.js';

export interface AutomationPlan {
  intent: TaskIntent;
  steps: AutomationStep[];
  requiredServices: string[];
  riskLevel: 'low' | 'medium' | 'high';
  requiresConfirmation: boolean;
  contextualInfo?: string;
  estimatedDuration?: number;
}

export interface TaskIntent {
  action: string;
  target: string;
  context: string;
  confidence: number;
  category: 'system' | 'file' | 'network' | 'development' | 'automation' | 'general';
  complexity: 'simple' | 'moderate' | 'complex';
}

export interface AutomationStep {
  id: string;
  type: 'terminal' | 'browser' | 'system' | 'wait';
  action: string;
  parameters: Record<string, any>;
  requiresAuth: boolean;
  description: string;
  expectedOutput?: string;
  fallbackActions?: string[];
  timeout?: number;
}

export interface ExecutionResult {
  success: boolean;
  output?: string;
  error?: string;
  duration: number;
  stepResults: StepResult[];
  contextLearned?: string[];
  suggestions?: string[];
}

export interface StepResult {
  stepId: string;
  success: boolean;
  output?: string;
  error?: string;
  duration: number;
  retryCount?: number;
}

export class DirectPromptingEngine {
  private genAI: GoogleGenerativeAI;
  private model: any;
  private commandParser: CommandParser;
  private taskPlanner: TaskPlanner;
  private osInfo: any;
  private conversationHistory: Array<{ input: string; output: string; timestamp: Date }> = [];
  private contextMemory: Map<string, any> = new Map();

  constructor() {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error('GEMINI_API_KEY is required for DirectPromptingEngine');
    }

    this.genAI = new GoogleGenerativeAI(apiKey);
    // Use Gemini 2.5 Pro for enhanced natural language understanding and multi-step reasoning
    this.model = this.genAI.getGenerativeModel({ 
      model: 'gemini-2.5-pro',
      generationConfig: {
        temperature: 0.1, // Lower temperature for more consistent command interpretation
        topK: 40,
        topP: 0.95,
        maxOutputTokens: 8192,
      },
    });
    this.commandParser = new CommandParser();
    this.taskPlanner = new TaskPlanner();
    this.osInfo = null;
  }

  /**
   * Initialize with OS information
   */
  public async initialize(): Promise<void> {
    try {
      const { FirstLaunchService } = await import('../setup/FirstLaunchService.js');
      const firstLaunchService = new FirstLaunchService();
      const config = await firstLaunchService.loadConfiguration();
      
      if (config?.osInfo) {
        this.osInfo = config.osInfo;
      } else {
        // Fallback: detect OS info directly
        this.osInfo = await firstLaunchService.detectOperatingSystem();
      }
    } catch (error) {
      console.warn('Could not load OS information:', error);
      // Set basic fallback OS info
      this.osInfo = {
        platform: process.platform === 'darwin' ? 'macos' : process.platform === 'win32' ? 'windows' : 'linux',
        version: 'unknown',
        architecture: process.arch,
        capabilities: { packageManagers: [] }
      };
    }
  }

  /**
   * Process natural language command using Gemini 2.5 Pro with context-aware understanding
   */
  public async processCommand(input: string): Promise<AutomationPlan> {
    StatusIndicator.info('Processing natural language command with Gemini 2.5 Pro...');

    try {
      // Initialize OS information if not already done
      if (!this.osInfo) {
        await this.initialize();
      }

      // Store conversation context
      this.addToConversationHistory(input);

      // Use Gemini 2.5 Pro for enhanced command understanding with context
      const intent = await this.analyzeIntentWithContext(input);
      
      // Perform multi-step task decomposition using AI
      const decomposition = await this.decomposeTask(input, intent);
      
      // Convert to structured command input with AI insights
      const commandInput: CommandInput = {
        mode: this.determineExecutionMode(intent),
        task: input,
        context: this.buildContextString(),
        isAlidoCommand: true
      };

      // Parse command using existing parser (enhanced with AI insights)
      const parsedCommand = await this.commandParser.parse(commandInput);
      
      // Create execution plan using existing planner with AI enhancements
      const plan = await this.taskPlanner.createPlan(parsedCommand);

      // Convert to our enhanced automation plan format
      const automationPlan: AutomationPlan = {
        intent,
        steps: this.convertToAutomationSteps(plan.steps, decomposition),
        requiredServices: this.determineRequiredServices(plan),
        riskLevel: plan.riskLevel,
        requiresConfirmation: plan.riskLevel !== 'low' || plan.requiresRoot,
        contextualInfo: this.generateContextualInfo(intent, plan),
        estimatedDuration: this.estimateExecutionDuration(plan.steps)
      };

      // Store successful processing in context memory
      this.contextMemory.set(`command_${Date.now()}`, {
        input,
        intent,
        plan: executionPlan,
        timestamp: new Date()
      });

      StatusIndicator.success('Command processed successfully with enhanced AI analysis');
      return automationPlan;

    } catch (error) {
      StatusIndicator.error('Failed to process command', {
        details: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  }

  /**
   * Analyze user intent using Gemini 2.5 Pro with enhanced context awareness
   */
  private async analyzeIntentWithContext(input: string): Promise<TaskIntent> {
    const osContext = this.buildOSContext();
    const conversationContext = this.buildConversationContext();
    
    const prompt = `You are an advanced AI assistant with deep understanding of system automation and user intent analysis.

SYSTEM CONTEXT:
${osContext}

CONVERSATION HISTORY:
${conversationContext}

CURRENT USER INPUT: "${input}"

Analyze this command with full context awareness and extract detailed intent information. Consider:
1. Previous commands and their outcomes
2. System capabilities and constraints
3. User patterns and preferences
4. Task complexity and requirements

Respond with JSON only:

{
  "action": "primary action verb (install, create, open, check, configure, etc.)",
  "target": "specific target of the action",
  "context": "additional context, parameters, or qualifiers",
  "confidence": 0.95,
  "category": "system|file|network|development|automation|general",
  "complexity": "simple|moderate|complex"
}

Examples for ${this.osInfo?.platform || 'linux'}:
- "install firefox and open it" → {"action": "install", "target": "firefox", "context": "then launch application", "confidence": 0.95, "category": "system", "complexity": "simple"}
- "create a development environment for React" → {"action": "create", "target": "development environment", "context": "React framework setup", "confidence": 0.9, "category": "development", "complexity": "complex"}
- "check system performance and optimize if needed" → {"action": "check", "target": "system performance", "context": "with optimization", "confidence": 0.85, "category": "system", "complexity": "moderate"}

Platform-specific considerations:
- ${this.osInfo?.platform === 'macos' ? 'macOS: Use brew for CLI tools, brew install --cask for GUI apps, open command for launching' : ''}
- ${this.osInfo?.platform === 'linux' ? 'Linux: Use native package manager (' + (this.osInfo?.capabilities?.packageManagers?.join(', ') || 'apt') + '), consider snap/flatpak alternatives' : ''}
- ${this.osInfo?.platform === 'windows' ? 'Windows: Use winget or chocolatey for packages, start command for launching' : ''}

Respond only with the JSON object.`;

    try {
      const result = await this.withTimeout(this.model.generateContent(prompt), 10000);
      const response = await result.response;
      const text = response.text();

      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const intent = JSON.parse(jsonMatch[0]) as TaskIntent;
        // Ensure all required fields are present
        return {
          action: intent.action || 'unknown',
          target: intent.target || input,
          context: intent.context || '',
          confidence: intent.confidence || 0.5,
          category: intent.category || 'general',
          complexity: intent.complexity || 'simple'
        };
      }

      // Fallback intent with enhanced structure
      return {
        action: 'unknown',
        target: input,
        context: '',
        confidence: 0.5,
        category: 'general',
        complexity: 'simple'
      };

    } catch (error) {
      console.warn('Enhanced intent analysis failed:', error);
      return {
        action: 'unknown',
        target: input,
        context: '',
        confidence: 0.3,
        category: 'general',
        complexity: 'simple'
      };
    }
  }

  /**
   * Decompose complex tasks into manageable steps using Gemini 2.5 Pro
   */
  private async decomposeTask(input: string, intent: TaskIntent): Promise<any> {
    if (intent.complexity === 'simple') {
      return null; // No decomposition needed for simple tasks
    }

    const osContext = this.buildOSContext();
    
    const prompt = `You are an expert system administrator breaking down complex automation tasks.

SYSTEM CONTEXT:
${osContext}

TASK: "${input}"
INTENT: ${JSON.stringify(intent)}

Break down this ${intent.complexity} task into logical, executable steps. Consider:
1. Prerequisites and dependencies
2. Error handling and fallbacks
3. Platform-specific implementations
4. Security and permission requirements

Respond with JSON only:

{
  "steps": [
    {
      "order": 1,
      "description": "Step description",
      "type": "terminal|browser|system|wait",
      "commands": ["command1", "command2"],
      "prerequisites": ["requirement1"],
      "fallbacks": ["alternative_command"],
      "riskLevel": "low|medium|high",
      "estimatedTime": 30
    }
  ],
  "totalSteps": 3,
  "estimatedDuration": 120,
  "riskAssessment": "overall risk level",
  "dependencies": ["tool1", "tool2"]
}

Focus on creating actionable, safe, and efficient step sequences for ${this.osInfo?.platform || 'this system'}.
Respond only with the JSON object.`;

    try {
      const result = await this.withTimeout(this.model.generateContent(prompt), 15000);
      const response = await result.response;
      const text = response.text();

      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }

      return null;

    } catch (error) {
      console.warn('Task decomposition failed:', error);
      return null;
    }
  }

  /**
   * Determine execution mode based on intent
   */
  private determineExecutionMode(intent: TaskIntent): ExecutionMode {
    const action = intent.action.toLowerCase();
    const target = intent.target.toLowerCase();

    // Browser-related actions
    if (action.includes('open') && (target.includes('browser') || target.includes('firefox') || target.includes('chrome'))) {
      return 'browser';
    }

    // Terminal operations (file operations will be handled through terminal commands)
    if (action.includes('create') || action.includes('delete') || action.includes('copy') || action.includes('move')) {
      return 'terminal';
    }

    // Default to auto mode for intelligent routing
    return 'auto';
  }

  /**
   * Convert plan steps to automation steps with AI decomposition insights
   */
  private convertToAutomationSteps(planSteps: any[], decomposition?: any): AutomationStep[] {
    const baseSteps = planSteps.map((step, index) => ({
      id: `step_${index + 1}`,
      type: step.type || 'terminal',
      action: step.command || step.action || '',
      parameters: step.parameters || {},
      requiresAuth: step.requiresAuth || false,
      description: step.description || `Execute: ${step.command || step.action}`,
      expectedOutput: step.expectedOutput,
      fallbackActions: step.fallbackSteps?.map((f: any) => f.command) || [],
      timeout: step.timeout || 30000
    }));

    // Enhance with AI decomposition if available
    if (decomposition?.steps) {
      return decomposition.steps.map((aiStep: any, index: number) => ({
        id: `ai_step_${index + 1}`,
        type: aiStep.type || 'terminal',
        action: aiStep.commands?.[0] || aiStep.description,
        parameters: {
          commands: aiStep.commands || [],
          prerequisites: aiStep.prerequisites || [],
          estimatedTime: aiStep.estimatedTime || 30
        },
        requiresAuth: aiStep.riskLevel === 'high' || aiStep.riskLevel === 'medium',
        description: aiStep.description,
        expectedOutput: aiStep.expectedOutput,
        fallbackActions: aiStep.fallbacks || [],
        timeout: (aiStep.estimatedTime || 30) * 1000
      }));
    }

    return baseSteps;
  }

  /**
   * Determine required services based on plan
   */
  private determineRequiredServices(plan: any): string[] {
    const services: string[] = [];

    // Check if browser automation is needed
    if (plan.steps.some((step: any) => step.type === 'browser')) {
      services.push('browser-automation');
    }

    // Check if system control is needed
    if (plan.steps.some((step: any) => step.requiresAuth || step.type === 'system')) {
      services.push('system-control');
    }

    // Check if file operations are needed
    if (plan.steps.some((step: any) => step.type === 'file')) {
      services.push('file-manager');
    }

    return services;
  }

  /**
   * Execute the automation plan
   */
  public async executeTask(plan: AutomationPlan): Promise<ExecutionResult> {
    const startTime = Date.now();
    const stepResults: StepResult[] = [];

    StatusIndicator.info(`Executing task: ${plan.intent.action} ${plan.intent.target}`);

    try {
      for (const step of plan.steps) {
        const stepStartTime = Date.now();
        
        StatusIndicator.info(`Executing step: ${step.description}`);

        try {
          // For now, we'll use the existing terminal execution
          // This will be enhanced with browser and system control in later tasks
          const result = await this.executeStep(step);
          
          const stepResult: StepResult = {
            stepId: step.id,
            success: true,
            output: result.output,
            duration: Date.now() - stepStartTime
          };

          stepResults.push(stepResult);
          StatusIndicator.success(`Step completed: ${step.description}`);

        } catch (error) {
          const stepResult: StepResult = {
            stepId: step.id,
            success: false,
            error: error instanceof Error ? error.message : String(error),
            duration: Date.now() - stepStartTime
          };

          stepResults.push(stepResult);
          StatusIndicator.error(`Step failed: ${step.description}`);
        }
      }

      const allSuccessful = stepResults.every(result => result.success);
      
      return {
        success: allSuccessful,
        duration: Date.now() - startTime,
        stepResults
      };

    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : String(error),
        duration: Date.now() - startTime,
        stepResults
      };
    }
  }

  /**
   * Execute individual step (placeholder for now)
   */
  private async executeStep(step: AutomationStep): Promise<{ output?: string }> {
    // This is a placeholder implementation
    // In later tasks, this will route to appropriate services (browser, system, etc.)
    
    if (step.type === 'terminal' && step.action) {
      // Use existing terminal engine
      const { TerminalEngine } = await import('../terminal/TerminalEngine.js');
      const terminalEngine = new TerminalEngine();
      
      const result = await terminalEngine.executeCommand(step.action);
      
      if (result.exitCode !== 0) {
        throw new Error(result.stderr || 'Command execution failed');
      }
      
      return { output: result.stdout };
    }

    // For other step types, return success for now
    return { output: `Step ${step.id} executed (placeholder)` };
  }

  /**
   * Build OS context string for prompts
   */
  private buildOSContext(): string {
    if (!this.osInfo) {
      return 'Operating System: Unknown';
    }

    const packageManagers = this.osInfo.capabilities?.packageManagers?.join(', ') || 'none detected';
    const capabilities = this.osInfo.capabilities || {};

    return `Operating System: ${this.osInfo.platform} ${this.osInfo.version} (${this.osInfo.architecture})
Available Package Managers: ${packageManagers}
System Capabilities:
- Node.js: ${capabilities.hasNodeJS ? 'Available' : 'Not available'}
- NPM: ${capabilities.hasNPM ? 'Available' : 'Not available'}
- Bash: ${capabilities.hasBash ? 'Available' : 'Not available'}
- Git: ${capabilities.hasGit ? 'Available' : 'Not available'}

Platform-specific notes:
${this.osInfo.platform === 'macos' ? '- Use "brew" for CLI tools, "brew install --cask" for GUI apps, "open" command to launch applications' : ''}
${this.osInfo.platform === 'linux' ? '- Use native package manager (' + (packageManagers || 'apt') + ') for system packages' : ''}
${this.osInfo.platform === 'windows' ? '- Use "winget" or "choco" for package management, "start" command to launch applications' : ''}`;
  }

  /**
   * Get contextual help for errors with enhanced AI analysis
   */
  public async getContextualHelp(error: string): Promise<string[]> {
    const osContext = this.buildOSContext();
    const conversationContext = this.buildConversationContext();
    
    const prompt = `You are an expert system administrator providing intelligent error resolution assistance.

SYSTEM CONTEXT:
${osContext}

CONVERSATION HISTORY:
${conversationContext}

ERROR: "${error}"

Analyze this error in context and provide 3-5 intelligent, actionable suggestions. Consider:
- Platform-specific solutions for ${this.osInfo?.platform || 'the current OS'}
- Available package managers: ${this.osInfo?.capabilities?.packageManagers?.join(', ') || 'system default'}
- Recent command history and patterns
- Common root causes and their solutions
- Progressive troubleshooting steps (simple to complex)
- Prevention strategies

Provide solutions in order of likelihood to resolve the issue.

Respond with a JSON array of detailed suggestion objects:
[
  {
    "suggestion": "Primary suggestion text",
    "commands": ["command1", "command2"],
    "explanation": "Why this might work",
    "riskLevel": "low|medium|high"
  }
]`;

    try {
      const result = await this.withTimeout(this.model.generateContent(prompt), 10000);
      const response = await result.response;
      const text = response.text();

      const jsonMatch = text.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        const suggestions = JSON.parse(jsonMatch[0]);
        return suggestions.map((s: any) => 
          typeof s === 'string' ? s : `${s.suggestion}${s.commands ? ` (${s.commands.join(', ')})` : ''}`
        );
      }

      return ['Check the error message for specific details', 'Verify system requirements', 'Try running with elevated permissions'];

    } catch (error) {
      return ['Unable to get contextual help at this time'];
    }
  }

  /**
   * Add conversation to history for context awareness
   */
  private addToConversationHistory(input: string, output?: string): void {
    this.conversationHistory.push({
      input,
      output: output || '',
      timestamp: new Date()
    });

    // Keep only last 10 interactions to manage memory
    if (this.conversationHistory.length > 10) {
      this.conversationHistory = this.conversationHistory.slice(-10);
    }
  }

  /**
   * Build conversation context string for AI prompts
   */
  private buildConversationContext(): string {
    if (this.conversationHistory.length === 0) {
      return 'No previous conversation history.';
    }

    const recentHistory = this.conversationHistory.slice(-5); // Last 5 interactions
    return recentHistory.map((entry, index) => 
      `${index + 1}. User: "${entry.input}" (${entry.timestamp.toLocaleTimeString()})`
    ).join('\n');
  }

  /**
   * Build context string for command processing
   */
  private buildContextString(): string {
    const contexts: string[] = [];
    
    // Add OS context
    contexts.push(`OS: ${this.osInfo?.platform || 'unknown'}`);
    
    // Add recent commands
    if (this.conversationHistory.length > 0) {
      const recent = this.conversationHistory.slice(-3).map(h => h.input).join(', ');
      contexts.push(`Recent: ${recent}`);
    }
    
    // Add memory context
    if (this.contextMemory.size > 0) {
      contexts.push(`Context items: ${this.contextMemory.size}`);
    }

    return contexts.join(' | ');
  }

  /**
   * Generate contextual information for execution plan
   */
  private generateContextualInfo(intent: TaskIntent, plan: any): string {
    const info: string[] = [];
    
    info.push(`Task Category: ${intent.category}`);
    info.push(`Complexity: ${intent.complexity}`);
    info.push(`Confidence: ${Math.round(intent.confidence * 100)}%`);
    
    if (plan.dependencies?.length > 0) {
      info.push(`Dependencies: ${plan.dependencies.join(', ')}`);
    }
    
    return info.join(' | ');
  }

  /**
   * Estimate execution duration based on steps
   */
  private estimateExecutionDuration(steps: any[]): number {
    let totalDuration = 0;
    
    for (const step of steps) {
      // Base duration by step type
      switch (step.type) {
        case 'terminal':
          totalDuration += 5000; // 5 seconds
          break;
        case 'browser':
          totalDuration += 10000; // 10 seconds
          break;
        case 'system':
          totalDuration += 3000; // 3 seconds
          break;
        case 'wait':
          totalDuration += 2000; // 2 seconds
          break;
        default:
          totalDuration += 5000;
      }
      
      // Add extra time for auth requirements
      if (step.requiresAuth) {
        totalDuration += 5000;
      }
      
      // Add extra time for complex commands
      if (step.command?.includes('install') || step.command?.includes('compile')) {
        totalDuration += 15000;
      }
    }
    
    return totalDuration;
  }

  /**
   * Timeout wrapper for AI requests
   */
  private async withTimeout<T>(promise: Promise<T>, timeoutMs: number): Promise<T> {
    const timeoutPromise = new Promise<never>((_, reject) => {
      setTimeout(() => reject(new Error(`AI request timeout after ${timeoutMs}ms`)), timeoutMs);
    });

    return Promise.race([promise, timeoutPromise]);
  }
}