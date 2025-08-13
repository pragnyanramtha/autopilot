package cli

import (
	"fmt"
	"strings"

	"github.com/spf13/cobra"
	"github.com/fatih/color"
)

var (
	// Color functions for terminal output
	successColor = color.New(color.FgGreen, color.Bold)
	errorColor   = color.New(color.FgRed, color.Bold)
	infoColor    = color.New(color.FgCyan)
	warningColor = color.New(color.FgYellow)
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "alvioli",
	Short: "AI-powered OS automation for Linux",
	Long: `Alvioli is a terminal-first AI automation system that can perform complex 
multi-step tasks across your Linux system using natural language commands.

Examples:
  alido install and open upscayl
  alido search for good wallpapers with a dark aesthetic
  ali ter "set up development environment"
  ali brw "generate mail summary"`,
	Version: "0.1.0",
}

// alidoCmd represents the main general-purpose command
var alidoCmd = &cobra.Command{
	Use:   "alido [task description...]",
	Short: "Execute general-purpose AI automation tasks",
	Long: `Execute any task using AI automation with automatic mode detection.
Everything after 'alido' is treated as a single command.

Examples:
  alido install and open upscayl
  alido search for good wallpapers with a dark aesthetic
  alido create a portfolio website from ~/resume.pdf`,
	Args: cobra.MinimumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		task := strings.Join(args, " ")
		executeTask(task, "auto", true)
	},
}

// aliCmd represents the ali command with subcommands
var aliCmd = &cobra.Command{
	Use:   "ali",
	Short: "AI automation with mode selection",
	Long: `Execute AI automation tasks with specific execution modes.
Use subcommands to specify terminal-first (ter) or browser-first (brw) execution.`,
}

// terCmd represents terminal-first execution
var terCmd = &cobra.Command{
	Use:   "ter [task description]",
	Short: "Execute task with terminal-first approach",
	Long: `Execute the task prioritizing terminal and command-line solutions.
Browser automation will only be used as a fallback.`,
	Args: cobra.MinimumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		task := strings.Join(args, " ")
		executeTask(task, "terminal", false)
	},
}

// brwCmd represents browser-first execution
var brwCmd = &cobra.Command{
	Use:   "brw [task description]",
	Short: "Execute task with browser-first approach",
	Long: `Execute the task prioritizing browser automation and web interactions.
Terminal commands will be used for supporting operations.`,
	Args: cobra.MinimumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		task := strings.Join(args, " ")
		executeTask(task, "browser", false)
	},
}

// doCmd represents auto-mode execution
var doCmd = &cobra.Command{
	Use:   "do [task description]",
	Short: "Execute task with automatic mode detection",
	Long: `Execute the task with automatic detection of the best execution mode
based on the task requirements and available tools.`,
	Args: cobra.MinimumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		task := strings.Join(args, " ")
		executeTask(task, "auto", false)
	},
}

func init() {
	// Add subcommands to ali
	aliCmd.AddCommand(terCmd)
	aliCmd.AddCommand(brwCmd)
	aliCmd.AddCommand(doCmd)

	// Add main commands to root
	rootCmd.AddCommand(alidoCmd)
	rootCmd.AddCommand(aliCmd)

	// Global flags
	rootCmd.PersistentFlags().BoolP("verbose", "v", false, "Enable verbose output")
	rootCmd.PersistentFlags().BoolP("dry-run", "n", false, "Show what would be executed without running")
	rootCmd.PersistentFlags().StringP("config", "c", "", "Config file path")
}

// Execute adds all child commands to the root command and sets flags appropriately.
func Execute() error {
	return rootCmd.Execute()
}

// executeTask is the main task execution function
func executeTask(task, mode string, isAlidoCommand bool) {
	infoColor.Printf("🤖 Alvioli AI Automation\n")
	fmt.Printf("Task: %s\n", task)
	fmt.Printf("Mode: %s\n", mode)
	
	if isAlidoCommand {
		infoColor.Printf("Using general-purpose alido command\n")
	}
	
	// TODO: Implement actual task execution
	// This is a placeholder for the core execution logic
	warningColor.Printf("⚠️  Task execution not yet implemented\n")
	fmt.Printf("This will be implemented in subsequent tasks.\n")
	
	// For now, just show what we would do
	successColor.Printf("✓ Command parsed successfully\n")
	fmt.Printf("Next steps:\n")
	fmt.Printf("  1. Parse natural language command\n")
	fmt.Printf("  2. Create execution plan\n")
	fmt.Printf("  3. Execute steps with error handling\n")
	fmt.Printf("  4. Provide summary of actions\n")
}