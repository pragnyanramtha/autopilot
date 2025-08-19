import { colors } from '../utils/Colors.js';
import { symbols } from '../utils/Symbols.js';
import { Layout } from '../utils/Layout.js';

export interface CommandInfo {
  name: string;
  description: string;
  usage?: string;
  aliases?: string[];
  options?: OptionInfo[];
  examples?: ExampleInfo[];
  subcommands?: CommandInfo[];
}

export interface OptionInfo {
  name: string;
  alias?: string;
  description: string;
  type?: 'string' | 'number' | 'boolean';
  required?: boolean;
  default?: any;
}

export interface ExampleInfo {
  command: string;
  description: string;
  output?: string;
}

export interface TroubleshootingStep {
  step: number;
  title: string;
  description: string;
  command?: string;
  expectedResult?: string;
}

export interface HelpDisplayOptions {
  showExamples?: boolean;
  showOptions?: boolean;
  showSubcommands?: boolean;
  compact?: boolean;
}

export class HelpDisplay {
  /**
   * Display formatted help for a command
   */
  static showCommand(command: CommandInfo, options: HelpDisplayOptions = {}): void {
    const {
      showExamples = true,
      showOptions = true,
      showSubcommands = true,
      compact = false
    } = options;

    console.log();
    
    // Command header
    console.log(colors.primary(colors.bold(`${command.name}`)));
    if (command.description) {
      console.log(colors.muted(command.description));
    }
    
    if (!compact) console.log();

    // Usage section
    if (command.usage) {
      console.log(colors.bold('USAGE'));
      console.log(Layout.indent(colors.primary(command.usage)));
      if (!compact) console.log();
    }

    // Aliases section
    if (command.aliases && command.aliases.length > 0) {
      console.log(colors.bold('ALIASES'));
      console.log(Layout.indent(command.aliases.join(', ')));
      if (!compact) console.log();
    }

    // Options section
    if (showOptions && command.options && command.options.length > 0) {
      console.log(colors.bold('OPTIONS'));
      this.displayOptions(command.options, compact);
      if (!compact) console.log();
    }

    // Subcommands section
    if (showSubcommands && command.subcommands && command.subcommands.length > 0) {
      console.log(colors.bold('COMMANDS'));
      this.displaySubcommands(command.subcommands, compact);
      if (!compact) console.log();
    }

    // Examples section
    if (showExamples && command.examples && command.examples.length > 0) {
      console.log(colors.bold('EXAMPLES'));
      this.displayExamples(command.examples, compact);
      if (!compact) console.log();
    }
  }

  /**
   * Display general help with command overview
   */
  static showGeneral(commands: CommandInfo[], appName: string = 'kira'): void {
    console.log();
    console.log(colors.primary(colors.bold(`${appName.toUpperCase()} - AI-Powered CLI Assistant`)));
    console.log(colors.muted('Intelligent command-line interface with AI assistance'));
    console.log();

    console.log(colors.bold('USAGE'));
    console.log(Layout.indent(colors.primary(`${appName} <command> [options]`)));
    console.log();

    console.log(colors.bold('AVAILABLE COMMANDS'));
    
    // Group commands by category if possible
    const categorizedCommands = this.categorizeCommands(commands);
    
    Object.entries(categorizedCommands).forEach(([category, cmds]) => {
      if (category !== 'general') {
        console.log();
        console.log(colors.info(category.toUpperCase()));
      }
      
      cmds.forEach(cmd => {
        const nameWithAliases = cmd.aliases && cmd.aliases.length > 0 
          ? `${cmd.name}, ${cmd.aliases.join(', ')}`
          : cmd.name;
        
        console.log(Layout.indent(
          `${colors.primary(nameWithAliases.padEnd(20))} ${colors.muted(cmd.description)}`
        ));
      });
    });

    console.log();
    console.log(colors.bold('GLOBAL OPTIONS'));
    console.log(Layout.indent(`${colors.primary('--help, -h'.padEnd(20))} ${colors.muted('Show help information')}`));
    console.log(Layout.indent(`${colors.primary('--version, -v'.padEnd(20))} ${colors.muted('Show version information')}`));
    console.log(Layout.indent(`${colors.primary('--verbose'.padEnd(20))} ${colors.muted('Enable verbose output')}`));
    console.log(Layout.indent(`${colors.primary('--debug'.padEnd(20))} ${colors.muted('Enable debug mode')}`));

    console.log();
    console.log(colors.info(`${symbols.info} Use '${appName} <command> --help' for more information about a command.`));
    console.log();
  }

  /**
   * Display troubleshooting steps
   */
  static showTroubleshooting(steps: TroubleshootingStep[], title: string = 'Troubleshooting'): void {
    console.log();
    console.log(colors.primary(colors.bold(title)));
    console.log(colors.muted(Layout.separator('─', title.length + 10)));
    console.log();

    steps.forEach(step => {
      console.log(colors.bold(`${step.step}. ${step.title}`));
      console.log(Layout.indent(step.description));
      
      if (step.command) {
        console.log();
        console.log(Layout.indent(colors.muted('Run:')));
        console.log(Layout.indent(colors.primary(`$ ${step.command}`), 2));
      }
      
      if (step.expectedResult) {
        console.log();
        console.log(Layout.indent(colors.muted('Expected result:')));
        console.log(Layout.indent(colors.success(step.expectedResult), 2));
      }
      
      console.log();
    });
  }

  /**
   * Display API key setup instructions
   */
  static showApiKeySetup(): void {
    const steps: TroubleshootingStep[] = [
      {
        step: 1,
        title: 'Get a Gemini API Key',
        description: 'Visit Google AI Studio to create a new API key.',
        command: 'open https://makersuite.google.com/app/apikey',
        expectedResult: 'Browser opens to Google AI Studio'
      },
      {
        step: 2,
        title: 'Create API Key',
        description: 'Click "Create API Key" and copy the generated key.',
        expectedResult: 'You have a new API key starting with "AIza..."'
      },
      {
        step: 3,
        title: 'Configure Kira',
        description: 'Run the initialization wizard to set up your API key.',
        command: 'kira init',
        expectedResult: 'API key is saved and Kira is ready to use'
      },
      {
        step: 4,
        title: 'Verify Setup',
        description: 'Test that Kira can connect to the Gemini API.',
        command: 'kira ask "Hello, are you working?"',
        expectedResult: 'Kira responds with an AI-generated message'
      }
    ];

    this.showTroubleshooting(steps, 'API Key Setup Guide');
    
    console.log(colors.warning(`${symbols.warning} Security Note:`));
    console.log(Layout.indent('Keep your API key secure and never share it publicly.'));
    console.log(Layout.indent('Add .env files to your .gitignore to prevent accidental commits.'));
    console.log();
  }

  /**
   * Display system requirements and setup
   */
  static showSystemRequirements(): void {
    console.log();
    console.log(colors.primary(colors.bold('System Requirements')));
    console.log(colors.muted(Layout.separator('─', 30)));
    console.log();

    console.log(colors.bold('Supported Platforms'));
    console.log(Layout.indent(`${symbols.success} Linux (Ubuntu, Debian, CentOS, Arch)`));
    console.log(Layout.indent(`${symbols.success} macOS (10.15 or later)`));
    console.log(Layout.indent(`${symbols.warning} Windows (experimental support)`));
    console.log();

    console.log(colors.bold('Required Software'));
    console.log(Layout.indent(`${symbols.bullet} Node.js 18.0 or later`));
    console.log(Layout.indent(`${symbols.bullet} npm or yarn package manager`));
    console.log(Layout.indent(`${symbols.bullet} Git (for version control features)`));
    console.log();

    console.log(colors.bold('Package Managers (at least one)'));
    console.log(Layout.indent(`${symbols.bullet} apt (Debian/Ubuntu)`));
    console.log(Layout.indent(`${symbols.bullet} yum/dnf (RedHat/CentOS/Fedora)`));
    console.log(Layout.indent(`${symbols.bullet} pacman (Arch Linux)`));
    console.log(Layout.indent(`${symbols.bullet} brew (macOS)`));
    console.log();

    console.log(colors.info(`${symbols.info} Run 'kira doctor' to check your system configuration.`));
    console.log();
  }

  /**
   * Display options in a formatted table
   */
  private static displayOptions(options: OptionInfo[], compact: boolean = false): void {
    const maxNameLength = Math.max(...options.map(opt => {
      const name = opt.alias ? `--${opt.name}, -${opt.alias}` : `--${opt.name}`;
      return name.length;
    }));

    options.forEach(option => {
      const name = option.alias ? `--${option.name}, -${option.alias}` : `--${option.name}`;
      const nameFormatted = colors.primary(name.padEnd(maxNameLength + 2));
      
      let description = option.description;
      
      // Add type information
      if (option.type && option.type !== 'boolean') {
        description += colors.muted(` (${option.type})`);
      }
      
      // Add default value
      if (option.default !== undefined) {
        description += colors.muted(` [default: ${option.default}]`);
      }
      
      // Add required indicator
      if (option.required) {
        description += colors.error(' *required*');
      }

      console.log(Layout.indent(`${nameFormatted} ${description}`));
    });
  }

  /**
   * Display subcommands in a formatted list
   */
  private static displaySubcommands(subcommands: CommandInfo[], compact: boolean = false): void {
    const maxNameLength = Math.max(...subcommands.map(cmd => cmd.name.length));

    subcommands.forEach(cmd => {
      const nameFormatted = colors.primary(cmd.name.padEnd(maxNameLength + 2));
      console.log(Layout.indent(`${nameFormatted} ${colors.muted(cmd.description)}`));
    });
  }

  /**
   * Display examples with syntax highlighting
   */
  private static displayExamples(examples: ExampleInfo[], compact: boolean = false): void {
    examples.forEach((example, index) => {
      if (index > 0 && !compact) console.log();
      
      console.log(Layout.indent(colors.muted(example.description)));
      console.log(Layout.indent(colors.primary(`$ ${example.command}`)));
      
      if (example.output) {
        console.log(Layout.indent(colors.muted('Output:')));
        console.log(Layout.indent(colors.dim(example.output), 2));
      }
    });
  }

  /**
   * Categorize commands for better organization
   */
  private static categorizeCommands(commands: CommandInfo[]): Record<string, CommandInfo[]> {
    const categories: Record<string, CommandInfo[]> = {
      general: []
    };

    commands.forEach(cmd => {
      // Simple categorization based on command name patterns
      if (cmd.name.includes('init') || cmd.name.includes('setup') || cmd.name.includes('config')) {
        if (!categories.setup) categories.setup = [];
        categories.setup.push(cmd);
      } else if (cmd.name.includes('ask') || cmd.name.includes('chat') || cmd.name.includes('ai')) {
        if (!categories.ai) categories.ai = [];
        categories.ai.push(cmd);
      } else if (cmd.name.includes('doctor') || cmd.name.includes('check') || cmd.name.includes('status')) {
        if (!categories.diagnostics) categories.diagnostics = [];
        categories.diagnostics.push(cmd);
      } else {
        categories.general.push(cmd);
      }
    });

    return categories;
  }
}