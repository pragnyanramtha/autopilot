package types

import (
	"context"
	"time"
)

// ExecutionMode defines how tasks should be executed
type ExecutionMode string

const (
	ModeTerminal ExecutionMode = "terminal"
	ModeBrowser  ExecutionMode = "browser"
	ModeAuto     ExecutionMode = "auto"
)

// TaskStepType defines the type of step in a task
type TaskStepType string

const (
	StepTerminal TaskStepType = "terminal"
	StepBrowser  TaskStepType = "browser"
	StepFile     TaskStepType = "file"
	StepWait     TaskStepType = "wait"
)

// TaskStatus defines the current status of a task execution
type TaskStatus string

const (
	StatusRunning     TaskStatus = "running"
	StatusCompleted   TaskStatus = "completed"
	StatusFailed      TaskStatus = "failed"
	StatusWaitingAuth TaskStatus = "waiting_auth"
)

// RiskLevel defines the risk level of an execution plan
type RiskLevel string

const (
	RiskLow    RiskLevel = "low"
	RiskMedium RiskLevel = "medium"
	RiskHigh   RiskLevel = "high"
)

// CommandInput represents user input for command processing
type CommandInput struct {
	Mode           ExecutionMode `json:"mode"`
	Task           string        `json:"task"`
	Context        string        `json:"context,omitempty"`
	IsAlidoCommand bool          `json:"is_alido_command"`
}

// ParsedCommand represents a parsed and analyzed command
type ParsedCommand struct {
	ExecutionMode       ExecutionMode `json:"execution_mode"`
	Steps               []TaskStep    `json:"steps"`
	RequiredTools       []string      `json:"required_tools"`
	EstimatedComplexity int           `json:"estimated_complexity"`
}

// TaskStep represents a single step in task execution
type TaskStep struct {
	ID            string       `json:"id"`
	Type          TaskStepType `json:"type"`
	Command       string       `json:"command,omitempty"`
	Selector      string       `json:"selector,omitempty"`
	ExpectedOutput string      `json:"expected_output,omitempty"`
	FallbackSteps []TaskStep   `json:"fallback_steps,omitempty"`
	RequiresAuth  bool         `json:"requires_auth"`
}

// ExecutionPlan represents a complete plan for task execution
type ExecutionPlan struct {
	Steps        []TaskStep `json:"steps"`
	Dependencies []string   `json:"dependencies"`
	RiskLevel    RiskLevel  `json:"risk_level"`
	RequiresRoot bool       `json:"requires_root"`
}

// CommandResult represents the result of a command execution
type CommandResult struct {
	ExitCode int           `json:"exit_code"`
	Stdout   string        `json:"stdout"`
	Stderr   string        `json:"stderr"`
	Duration time.Duration `json:"duration"`
}

// TaskExecution represents a complete task execution session
type TaskExecution struct {
	ID              string         `json:"id"`
	OriginalCommand string         `json:"original_command"`
	Mode            ExecutionMode  `json:"mode"`
	Steps           []ExecutedStep `json:"steps"`
	Status          TaskStatus     `json:"status"`
	StartTime       time.Time      `json:"start_time"`
	EndTime         *time.Time     `json:"end_time,omitempty"`
	Context         map[string]any `json:"context"`
}

// ExecutedStep represents a step that has been executed
type ExecutedStep struct {
	Step       TaskStep       `json:"step"`
	Result     *CommandResult `json:"result,omitempty"`
	Error      string         `json:"error,omitempty"`
	RetryCount int            `json:"retry_count"`
	Duration   time.Duration  `json:"duration"`
}

// CommandError represents an error that occurred during command execution
type CommandError struct {
	Command   string `json:"command"`
	ExitCode  int    `json:"exit_code"`
	Stderr    string `json:"stderr"`
	Timestamp time.Time `json:"timestamp"`
}

// RetryStrategy represents a strategy for retrying failed commands
type RetryStrategy struct {
	ShouldRetry     bool     `json:"should_retry"`
	AlternativeCmd  string   `json:"alternative_cmd,omitempty"`
	DelaySeconds    int      `json:"delay_seconds"`
	MaxRetries      int      `json:"max_retries"`
	SearchSolutions bool     `json:"search_solutions"`
}

// Solution represents a potential solution for a command error
type Solution struct {
	Description string   `json:"description"`
	Commands    []string `json:"commands"`
	Source      string   `json:"source"`
	Confidence  float64  `json:"confidence"`
}

// ContextData represents stored context information
type ContextData struct {
	Key            string    `json:"key"`
	Value          string    `json:"value"`
	Context        string    `json:"context"`
	RelevanceScore float64   `json:"relevance_score"`
	CreatedAt      time.Time `json:"created_at"`
	ExpiresAt      *time.Time `json:"expires_at,omitempty"`
}

// SessionData represents session history data
type SessionData struct {
	ID        string    `json:"id"`
	Command   string    `json:"command"`
	Success   bool      `json:"success"`
	Timestamp time.Time `json:"timestamp"`
	Duration  time.Duration `json:"duration"`
}

// Interfaces for core components

// CommandParser interface for parsing user commands
type CommandParser interface {
	Parse(input CommandInput) (*ParsedCommand, error)
	DetectMode(task string) ExecutionMode
	ExtractContext(task string) map[string]any
}

// TaskPlanner interface for planning task execution
type TaskPlanner interface {
	CreatePlan(cmd *ParsedCommand) (*ExecutionPlan, error)
	BreakdownTask(task string, mode ExecutionMode) ([]TaskStep, error)
	EstimateComplexity(steps []TaskStep) int
}

// TerminalEngine interface for terminal command execution
type TerminalEngine interface {
	ExecuteCommand(ctx context.Context, command string) (*CommandResult, error)
	HandleError(error *CommandError) (*RetryStrategy, error)
	SearchSolution(error string) ([]Solution, error)
	RequestRootAccess(reason string) (bool, error)
}

// BrowserEngine interface for browser automation
type BrowserEngine interface {
	LaunchBrowser(ctx context.Context) error
	NavigateToURL(ctx context.Context, url string) error
	WaitForAuth(ctx context.Context) error
	ExtractContent(ctx context.Context, selector string) (string, error)
	DetectLoginScreen(ctx context.Context) (bool, error)
	Close() error
}

// ContextManager interface for context and memory management
type ContextManager interface {
	StoreInformation(key, value, context string) error
	RetrieveRelevant(task string) ([]ContextData, error)
	UpdateLearning(command string, success bool) error
	GetSessionHistory() ([]SessionData, error)
}

// ExecutionCoordinator interface for coordinating task execution
type ExecutionCoordinator interface {
	Execute(ctx context.Context, plan *ExecutionPlan) (*TaskExecution, error)
	HandleStepFailure(step *TaskStep, error *CommandError) (*RetryStrategy, error)
	SwitchMode(from, to ExecutionMode) error
}