import { GeminiService } from './GeminiService.js';
import { StatusIndicator } from '../ui/components/StatusIndicator.js';
import chalk from 'chalk';

export interface SystemAnalysis {
  recommendedPackageManager: string;
  packageManagerReason: string;
  setupRecommendations: string[];
  missingTools: string[];
  optimizations: string[];
  securityNotes: string[];
}

export interface SystemData {
  platform: string;
  os_release: any;
  system: any;
  hardware: any;
  package_managers: any;
  development_tools: any;
  network: any;
  distribution: any;
}

export class SystemAnalyzer {
  private geminiService: GeminiService;

  constructor() {
    this.geminiService = new GeminiService();
  }

  /**
   * Analyze system data using AI to provide intelligent recommendations
   */
  async analyzeSystem(systemData: SystemData): Promise<SystemAnalysis> {
    StatusIndicator.info('Analyzing system with AI...');

    if (!this.geminiService.isAIEnabled()) {
      // Fallback to rule-based analysis if AI is not available
      return this.fallbackAnalysis(systemData);
    }

    try {
      const prompt = this.buildAnalysisPrompt(systemData);
      const response = await this.geminiService.generateResponse(prompt);
      
      // Parse AI response
      const analysis = this.parseAIResponse(response, systemData);
      
      StatusIndicator.success('AI analysis completed');
      return analysis;

    } catch (error) {
      StatusIndicator.warning('AI analysis failed, using fallback method');
      console.warn('AI analysis error:', error);
      return this.fallbackAnalysis(systemData);
    }
  }

  /**
   * Build comprehensive prompt for AI analysis
   */
  private buildAnalysisPrompt(systemData: SystemData): string {
    const availablePackageManagers = Object.entries(systemData.package_managers)
      .filter(([_, data]: [string, any]) => data.available)
      .map(([name, data]: [string, any]) => `${name} (v${data.version})`);

    const availableTools = Object.entries(systemData.development_tools)
      .filter(([_, data]: [string, any]) => data.available)
      .map(([name, data]: [string, any]) => `${name} (v${data.version})`);

    const missingTools = Object.entries(systemData.development_tools)
      .filter(([_, data]: [string, any]) => !data.available)
      .map(([name, _]: [string, any]) => name);

    return `You are an expert system administrator analyzing a ${systemData.platform} system for optimal package management and development setup.

SYSTEM INFORMATION:
- Platform: ${systemData.platform}
- OS: ${systemData.os_release?.PRETTY_NAME || systemData.os_release?.NAME || 'Unknown'}
- Architecture: ${systemData.system?.architecture || 'Unknown'}
- Distribution Family: ${systemData.distribution?.family || 'Unknown'}
- CPU: ${systemData.hardware?.cpu_model || 'Unknown'}
- Memory: ${systemData.hardware?.memory_total || 'Unknown'}

AVAILABLE PACKAGE MANAGERS:
${availablePackageManagers.length > 0 ? availablePackageManagers.join(', ') : 'None detected'}

INSTALLED DEVELOPMENT TOOLS:
${availableTools.length > 0 ? availableTools.join(', ') : 'None detected'}

MISSING DEVELOPMENT TOOLS:
${missingTools.length > 0 ? missingTools.join(', ') : 'All common tools are installed'}

CURRENT PRIMARY PACKAGE MANAGER:
${systemData.distribution?.primary_package_manager || 'Unknown'}

SPECIAL CONSIDERATIONS:
${systemData.platform === 'darwin' ? '- macOS system with potential for Homebrew' : ''}
${systemData.platform === 'linux' ? `- Linux distribution: ${systemData.distribution?.family}` : ''}
${systemData.platform === 'win32' ? '- Windows system with winget/chocolatey options' : ''}
${systemData.distribution?.homebrew_installed === false && systemData.platform === 'darwin' ? '- Homebrew is NOT installed on macOS' : ''}

Please analyze this system and provide recommendations in the following JSON format:
{
  "recommendedPackageManager": "primary_manager_name",
  "packageManagerReason": "detailed_explanation_why_this_manager_is_best",
  "setupRecommendations": [
    "specific_actionable_recommendation_1",
    "specific_actionable_recommendation_2"
  ],
  "missingTools": [
    "essential_tool_1",
    "essential_tool_2"
  ],
  "optimizations": [
    "performance_optimization_1",
    "workflow_optimization_2"
  ],
  "securityNotes": [
    "security_consideration_1",
    "security_best_practice_2"
  ]
}

ANALYSIS CRITERIA:
1. Choose the BEST package manager for this specific system configuration
2. Consider the user's development workflow and available tools
3. Prioritize stability, security, and ease of use
4. For macOS without Homebrew, strongly recommend installing it
5. For Linux, respect the distribution's native package manager but suggest alternatives if beneficial
6. For Windows, recommend modern package managers like winget
7. Provide specific, actionable recommendations
8. Focus on practical improvements the user can implement immediately

Respond ONLY with the JSON object, no additional text.`;
  }

  /**
   * Parse AI response into structured analysis
   */
  private parseAIResponse(response: string, systemData: SystemData): SystemAnalysis {
    try {
      // Clean the response to extract JSON
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        throw new Error('No JSON found in AI response');
      }

      const analysis = JSON.parse(jsonMatch[0]);
      
      // Validate required fields
      if (!analysis.recommendedPackageManager || !analysis.packageManagerReason) {
        throw new Error('Invalid AI response structure');
      }

      return {
        recommendedPackageManager: analysis.recommendedPackageManager,
        packageManagerReason: analysis.packageManagerReason,
        setupRecommendations: analysis.setupRecommendations || [],
        missingTools: analysis.missingTools || [],
        optimizations: analysis.optimizations || [],
        securityNotes: analysis.securityNotes || []
      };

    } catch (error) {
      console.warn('Failed to parse AI response:', error);
      return this.fallbackAnalysis(systemData);
    }
  }

  /**
   * Fallback rule-based analysis when AI is not available
   */
  private fallbackAnalysis(systemData: SystemData): SystemAnalysis {
    const platform = systemData.platform;
    const availableManagers = Object.entries(systemData.package_managers)
      .filter(([_, data]: [string, any]) => data.available)
      .map(([name, _]: [string, any]) => name);

    let recommendedManager = 'unknown';
    let reason = 'Unable to determine optimal package manager';
    const recommendations: string[] = [];
    const missingTools: string[] = [];
    const optimizations: string[] = [];
    const securityNotes: string[] = [];

    // Platform-specific logic
    if (platform === 'darwin') {
      if (availableManagers.includes('brew')) {
        recommendedManager = 'brew';
        reason = 'Homebrew is the standard package manager for macOS and provides the best compatibility';
      } else {
        recommendedManager = 'brew';
        reason = 'Homebrew should be installed as it is essential for macOS development';
        recommendations.push('Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"');
      }
      recommendations.push('Install Xcode Command Line Tools if not already installed');
      optimizations.push('Use Homebrew Cask for GUI applications');
    } else if (platform === 'linux') {
      const family = systemData.distribution?.family;
      if (family === 'debian' && availableManagers.includes('apt')) {
        recommendedManager = 'apt';
        reason = 'APT is the native package manager for Debian-based systems and provides the best integration';
      } else if (family === 'redhat' && availableManagers.includes('dnf')) {
        recommendedManager = 'dnf';
        reason = 'DNF is the modern package manager for Red Hat-based systems';
      } else if (family === 'redhat' && availableManagers.includes('yum')) {
        recommendedManager = 'yum';
        reason = 'YUM is the traditional package manager for Red Hat-based systems';
      } else if (family === 'arch' && availableManagers.includes('pacman')) {
        recommendedManager = 'pacman';
        reason = 'Pacman is the native package manager for Arch Linux';
      } else if (availableManagers.length > 0) {
        recommendedManager = availableManagers[0];
        reason = `Using ${availableManagers[0]} as it is available on your system`;
      }
      
      if (availableManagers.includes('snap')) {
        optimizations.push('Consider using Snap for cross-distribution packages');
      }
      if (availableManagers.includes('flatpak')) {
        optimizations.push('Consider using Flatpak for sandboxed applications');
      }
    } else if (platform === 'win32') {
      if (availableManagers.includes('winget')) {
        recommendedManager = 'winget';
        reason = 'Windows Package Manager (winget) is the official Microsoft package manager';
      } else if (availableManagers.includes('choco')) {
        recommendedManager = 'choco';
        reason = 'Chocolatey is a mature package manager for Windows';
      } else {
        recommendedManager = 'winget';
        reason = 'Windows Package Manager should be installed for the best Windows experience';
        recommendations.push('Install winget from Microsoft Store or GitHub');
      }
    }

    // Check for missing essential tools
    const essentialTools = ['git', 'curl', 'node', 'npm'];
    essentialTools.forEach(tool => {
      if (!systemData.development_tools[tool]?.available) {
        missingTools.push(tool);
      }
    });

    // General recommendations
    if (missingTools.length > 0) {
      recommendations.push(`Install essential development tools: ${missingTools.join(', ')}`);
    }

    // Security notes
    securityNotes.push('Keep your package manager and system updated regularly');
    securityNotes.push('Only install packages from trusted sources');

    return {
      recommendedPackageManager: recommendedManager,
      packageManagerReason: reason,
      setupRecommendations: recommendations,
      missingTools,
      optimizations,
      securityNotes
    };
  }

  /**
   * Display analysis results in a user-friendly format
   */
  displayAnalysis(analysis: SystemAnalysis): void {
    console.log(chalk.cyan.bold('\n🤖 AI System Analysis Results\n'));

    // Recommended Package Manager
    console.log(chalk.green.bold('📦 Recommended Package Manager:'));
    console.log(`   ${chalk.yellow(analysis.recommendedPackageManager)}`);
    console.log(`   ${chalk.gray(analysis.packageManagerReason)}\n`);

    // Setup Recommendations
    if (analysis.setupRecommendations.length > 0) {
      console.log(chalk.blue.bold('🔧 Setup Recommendations:'));
      analysis.setupRecommendations.forEach((rec, index) => {
        console.log(`   ${index + 1}. ${rec}`);
      });
      console.log();
    }

    // Missing Tools
    if (analysis.missingTools.length > 0) {
      console.log(chalk.yellow.bold('⚠️  Missing Essential Tools:'));
      analysis.missingTools.forEach(tool => {
        console.log(`   • ${tool}`);
      });
      console.log();
    }

    // Optimizations
    if (analysis.optimizations.length > 0) {
      console.log(chalk.magenta.bold('⚡ Optimization Suggestions:'));
      analysis.optimizations.forEach((opt, index) => {
        console.log(`   ${index + 1}. ${opt}`);
      });
      console.log();
    }

    // Security Notes
    if (analysis.securityNotes.length > 0) {
      console.log(chalk.red.bold('🔒 Security Considerations:'));
      analysis.securityNotes.forEach((note, index) => {
        console.log(`   ${index + 1}. ${note}`);
      });
      console.log();
    }
  }
}