import { GoogleGenerativeAI } from '@google/generative-ai';
import * as dotenv from 'dotenv';
import { ProfileManager } from '../profile/ProfileManager.js';

// Load environment variables
dotenv.config();

export interface AICommandAnalysis {
  intent: string;
  confidence: number;
  suggestedCommands: string[];
  executionMode: 'terminal' | 'browser' | 'file';
  riskLevel: 'low' | 'medium' | 'high';
  requiresRoot: boolean;
  explanation: string;
}

export interface AIErrorSolution {
  description: string;
  commands: string[];
  confidence: number;
  reasoning: string;
}

export class GeminiService {
  private genAI: GoogleGenerativeAI | null = null;
  private model: any = null;
  private isEnabled: boolean = false;

  constructor() {
    // Temporarily disable AI for testing
    const apiKey = process.env.GEMINI_API_KEY ;

    if (apiKey && apiKey !== 'your_gemini_api_key_here') {
      try {
        this.genAI = new GoogleGenerativeAI(apiKey);
        // Prioritize Gemini 2.5 Flash for speed and efficiency
        this.model = this.genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
        this.isEnabled = true;
        console.log('🤖 Gemini AI service initialized with Flash model');
      } catch (error) {
        console.warn('⚠️  Failed to initialize Gemini AI:', error instanceof Error ? error.message : String(error));
        this.isEnabled = false;
      }
    } else {
      console.log('ℹ️  Gemini API key not provided. Using built-in command parsing.');
      this.isEnabled = false;
    }
  }

  async analyzeCommand(userInput: string): Promise<AICommandAnalysis | null> {
    if (!this.isEnabled || !this.model) {
      return null;
    }

    try {
      return await this.withTimeout(this.performAnalysis(userInput), 8000);
    } catch (error) {
      console.warn('⚠️  Gemini API error:', error instanceof Error ? error.message : String(error));
      return null;
    }
  }

  private async performAnalysis(userInput: string): Promise<AICommandAnalysis | null> {
    try {
      // Get user context from profile
      const profileManager = ProfileManager.getInstance();
      const userContext = await profileManager.getAIContext();
      const userName = await profileManager.getUserName();
      
      const prompt = `
You are Kira, an intelligent AI assistant for Linux automation. You have access to the user's profile and system information.

${userContext}

User Input: "${userInput}"
User Name: ${userName}

Please analyze this command and respond with a JSON object containing:
1. intent: What the user wants to accomplish (brief description)
2. confidence: How confident you are in understanding (0.0-1.0)
3. suggestedCommands: Array of actual Linux commands to execute
4. executionMode: "terminal", "browser", or "file"
5. riskLevel: "low", "medium", or "high"
6. requiresRoot: boolean if sudo/root access needed
7. explanation: Brief explanation of what will happen

Focus on:
- Converting natural language to actual Linux commands
- ALWAYS use bash shell syntax and commands
- Prioritizing terminal/CLI solutions over GUI
- Using package managers: apt, snap, flatpak, pacman
- Being security-conscious
- Providing safe, tested bash commands

Example response format:
{
  "intent": "Install and launch image upscaler application",
  "confidence": 0.9,
  "suggestedCommands": ["sudo apt update", "sudo apt install upscayl", "upscayl &"],
  "executionMode": "terminal",
  "riskLevel": "low",
  "requiresRoot": true,
  "explanation": "Updates package list, installs upscayl via apt, then launches it in background"
}

Respond only with valid JSON.
`;

      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      const text = response.text();

      // Extract JSON from response
      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const analysis = JSON.parse(jsonMatch[0]);
        return analysis as AICommandAnalysis;
      }

      return null;
    } catch (error) {
      throw error; // Re-throw to be caught by withTimeout wrapper
    }
  }

  async findErrorSolution(command: string, errorMessage: string): Promise<AIErrorSolution | null> {
    if (!this.isEnabled || !this.model) {
      return null;
    }

    try {
      return await this.withTimeout(this.performErrorAnalysis(command, errorMessage), 8000);
    } catch (error) {
      console.warn('⚠️  Gemini AI error for solution search:', error instanceof Error ? error.message : String(error));
      return null;
    }
  }

  private async performErrorAnalysis(command: string, errorMessage: string): Promise<AIErrorSolution | null> {
    try {
      // Get user context from profile
      const profileManager = ProfileManager.getInstance();
      const userContext = await profileManager.getAIContext();
      const userName = await profileManager.getUserName();
      
      const prompt = `
You are Kira, an intelligent AI assistant helping ${userName} with Linux automation. You have access to their system information and preferences.

${userContext}

Failed Command: "${command}"
Error Message: "${errorMessage}"

INTELLIGENT ERROR ANALYSIS REQUIRED:

1. If "command not found":
   - Is this a program that can be installed? (e.g., firefox, git, docker, etc.)
   - Is this a core system command that should exist? (e.g., apt, yum, pacman)
   - If core command missing, detect the Linux distribution and suggest the correct package manager

2. If package manager command failed:
   - Detect which distribution this likely is based on the error
   - Suggest the correct package manager for this distro:
     * Debian/Ubuntu: apt, apt-get
     * Arch/Manjaro: pacman, yay
     * RHEL/CentOS/Fedora: yum, dnf
     * openSUSE: zypper
     * Alpine: apk

3. Provide step-by-step solution as JSON:
{
  "description": "Intelligent analysis of the problem and solution",
  "commands": ["step1_command", "step2_command", "step3_command"],
  "confidence": 0.9,
  "reasoning": "Detailed explanation of the analysis and why this solution works"
}

EXAMPLES:
- If "apt: command not found" → Detect non-Debian system, suggest pacman/yum/dnf
- If "firefox: command not found" → Install firefox using detected package manager
- If "git: command not found" → Install git development tools

Focus on:
- Distribution detection and appropriate package manager selection
- Intelligent program vs system command differentiation
- Safe, tested BASH commands for the detected system
- Step-by-step installation and configuration

ALWAYS use bash shell syntax and built-in commands.
Respond only with valid JSON.
`;

      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      const text = response.text();

      // Extract JSON from response
      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const solution = JSON.parse(jsonMatch[0]);
        return solution as AIErrorSolution;
      }

      return null;
    } catch (error) {
      throw error;
    }
  }

  async improveCommand(originalCommand: string, context?: string): Promise<string | null> {
    if (!this.isEnabled || !this.model) {
      return null;
    }

    try {
      const prompt = `
You are a Linux command optimization expert. Improve this command to be more robust and safe.

Original Command: "${originalCommand}"
${context ? `Context: ${context}` : ''}

Provide an improved version that:
- Adds appropriate error handling
- Uses safer flags/options
- Includes necessary prerequisites
- Follows Linux best practices
- USES BASH SHELL SYNTAX ONLY

Respond with just the improved bash command, no explanation.
`;

      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      const text = response.text().trim();

      // Remove any markdown formatting
      const cleanCommand = text.replace(/```bash\n?|```\n?/g, '').trim();

      return cleanCommand || null;
    } catch (error) {
      console.warn('⚠️  Gemini API error for command improvement:', error instanceof Error ? error.message : String(error));
      return null;
    }
  }

  isAIEnabled(): boolean {
    return this.isEnabled;
  }

  private async withTimeout<T>(promise: Promise<T>, timeoutMs: number = 8000): Promise<T> {
    const timeoutPromise = new Promise<never>((_, reject) => {
      setTimeout(() => reject(new Error(`AI request timeout after ${timeoutMs}ms`)), timeoutMs);
    });

    return Promise.race([promise, timeoutPromise]);
  }

  private async switchToProModel(): Promise<any> {
    if (!this.genAI) return null;

    try {
      console.log('🔄 Switching to Gemini Pro for complex reasoning...');
      return this.genAI.getGenerativeModel({ model: 'gemini-1.5-pro' });
    } catch (error) {
      console.warn('⚠️  Failed to switch to Pro model:', error instanceof Error ? error.message : String(error));
      return this.model; // Fallback to current model
    }
  }

  async analyzeComplexCommand(userInput: string): Promise<AICommandAnalysis | null> {
    // Use Pro model for complex multi-step commands
    if (!this.isEnabled || !this.genAI) {
      return null;
    }

    const proModel = await this.switchToProModel();
    if (!proModel) return null;

    try {
      const prompt = `
You are an expert Linux system administrator analyzing a complex automation request. This requires deep understanding and multi-step planning.

User Input: "${userInput}"

Analyze this complex command and provide detailed JSON response:
{
  "intent": "Detailed description of what user wants to accomplish",
  "confidence": 0.95,
  "suggestedCommands": ["step1", "step2", "step3"],
  "executionMode": "terminal|browser|file",
  "riskLevel": "low|medium|high",
  "requiresRoot": true/false,
  "explanation": "Detailed explanation of the complete workflow"
}

Focus on:
- Breaking down complex workflows into safe, executable steps
- Handling dependencies and prerequisites
- Error prevention and safety checks
- Optimal command sequencing

Respond only with valid JSON.
`;

      const result = await proModel.generateContent(prompt);
      const response = await result.response;
      const text = response.text();

      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const analysis = JSON.parse(jsonMatch[0]);
        return analysis as AICommandAnalysis;
      }

      return null;
    } catch (error) {
      console.warn('⚠️  Gemini Pro API error:', error instanceof Error ? error.message : String(error));
      return null;
    }
  }
}