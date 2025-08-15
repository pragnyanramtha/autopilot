import { GoogleGenerativeAI } from '@google/generative-ai';
import * as dotenv from 'dotenv';

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
    // Use provided API key or fallback to environment variable
    const apiKey = process.env.GEMINI_API_KEY || 'AIzaSyBP8VGRnBcG-fi35O51F4gXgq7aqWTLn-U';
    
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
      const prompt = `
You are an expert Linux system administrator and automation specialist. Analyze this user command and provide a structured response.

User Input: "${userInput}"

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
- Prioritizing terminal/CLI solutions over GUI
- Using package managers: apt, snap, flatpak
- Being security-conscious
- Providing safe, tested commands

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
      console.warn('⚠️  Gemini API error:', error instanceof Error ? error.message : String(error));
      return null;
    }
  }

  async findErrorSolution(command: string, errorMessage: string): Promise<AIErrorSolution | null> {
    if (!this.isEnabled || !this.model) {
      return null;
    }

    try {
      const prompt = `
You are a Linux troubleshooting expert. Help solve this command error.

Failed Command: "${command}"
Error Message: "${errorMessage}"

Analyze the error and provide a solution as JSON:
{
  "description": "Brief description of the problem and solution",
  "commands": ["array", "of", "commands", "to", "fix", "it"],
  "confidence": 0.8,
  "reasoning": "Explanation of why this solution should work"
}

Focus on:
- Common Linux error patterns
- Package installation issues
- Permission problems
- Missing dependencies
- Network connectivity
- Disk space issues

Provide practical, safe commands that will likely resolve the issue.
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
      console.warn('⚠️  Gemini API error for solution search:', error instanceof Error ? error.message : String(error));
      return null;
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

Respond with just the improved command, no explanation.
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