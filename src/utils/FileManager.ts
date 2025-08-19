import * as fs from 'fs';
import * as path from 'path';
import { StatusIndicator } from '../ui/components/StatusIndicator.js';

export interface FileOperation {
  success: boolean;
  message: string;
  data?: any;
}

export class FileManager {
  /**
   * Read a file and return its contents
   */
  public static readFile(filePath: string): FileOperation {
    try {
      if (!fs.existsSync(filePath)) {
        return {
          success: false,
          message: `File not found: ${filePath}`
        };
      }

      const content = fs.readFileSync(filePath, 'utf8');
      return {
        success: true,
        message: `Successfully read file: ${filePath}`,
        data: content
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to read file: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Write content to a file
   */
  public static writeFile(filePath: string, content: string, options?: { createDir?: boolean }): FileOperation {
    try {
      // Create directory if it doesn't exist and createDir is true
      if (options?.createDir) {
        const dir = path.dirname(filePath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }
      }

      fs.writeFileSync(filePath, content, 'utf8');
      return {
        success: true,
        message: `Successfully wrote file: ${filePath}`,
        data: { path: filePath, size: content.length }
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to write file: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Append content to a file
   */
  public static appendFile(filePath: string, content: string, options?: { createDir?: boolean }): FileOperation {
    try {
      // Create directory if it doesn't exist and createDir is true
      if (options?.createDir) {
        const dir = path.dirname(filePath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }
      }

      fs.appendFileSync(filePath, content, 'utf8');
      return {
        success: true,
        message: `Successfully appended to file: ${filePath}`,
        data: { path: filePath, appendedSize: content.length }
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to append to file: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Check if a file exists
   */
  public static fileExists(filePath: string): boolean {
    return fs.existsSync(filePath);
  }

  /**
   * Get file information
   */
  public static getFileInfo(filePath: string): FileOperation {
    try {
      if (!fs.existsSync(filePath)) {
        return {
          success: false,
          message: `File not found: ${filePath}`
        };
      }

      const stats = fs.statSync(filePath);
      return {
        success: true,
        message: `File info retrieved: ${filePath}`,
        data: {
          path: filePath,
          size: stats.size,
          isFile: stats.isFile(),
          isDirectory: stats.isDirectory(),
          created: stats.birthtime,
          modified: stats.mtime,
          accessed: stats.atime
        }
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to get file info: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * List files in a directory
   */
  public static listDirectory(dirPath: string): FileOperation {
    try {
      if (!fs.existsSync(dirPath)) {
        return {
          success: false,
          message: `Directory not found: ${dirPath}`
        };
      }

      const stats = fs.statSync(dirPath);
      if (!stats.isDirectory()) {
        return {
          success: false,
          message: `Path is not a directory: ${dirPath}`
        };
      }

      const files = fs.readdirSync(dirPath);
      const fileDetails = files.map(file => {
        const filePath = path.join(dirPath, file);
        const fileStats = fs.statSync(filePath);
        return {
          name: file,
          path: filePath,
          isFile: fileStats.isFile(),
          isDirectory: fileStats.isDirectory(),
          size: fileStats.size,
          modified: fileStats.mtime
        };
      });

      return {
        success: true,
        message: `Directory listing for: ${dirPath}`,
        data: {
          path: dirPath,
          files: fileDetails,
          count: files.length
        }
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to list directory: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Create a directory
   */
  public static createDirectory(dirPath: string, options?: { recursive?: boolean }): FileOperation {
    try {
      if (fs.existsSync(dirPath)) {
        return {
          success: false,
          message: `Directory already exists: ${dirPath}`
        };
      }

      fs.mkdirSync(dirPath, { recursive: options?.recursive || false });
      return {
        success: true,
        message: `Successfully created directory: ${dirPath}`,
        data: { path: dirPath }
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to create directory: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Delete a file
   */
  public static deleteFile(filePath: string): FileOperation {
    try {
      if (!fs.existsSync(filePath)) {
        return {
          success: false,
          message: `File not found: ${filePath}`
        };
      }

      const stats = fs.statSync(filePath);
      if (!stats.isFile()) {
        return {
          success: false,
          message: `Path is not a file: ${filePath}`
        };
      }

      fs.unlinkSync(filePath);
      return {
        success: true,
        message: `Successfully deleted file: ${filePath}`,
        data: { path: filePath }
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to delete file: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Copy a file
   */
  public static copyFile(sourcePath: string, destPath: string, options?: { createDir?: boolean }): FileOperation {
    try {
      if (!fs.existsSync(sourcePath)) {
        return {
          success: false,
          message: `Source file not found: ${sourcePath}`
        };
      }

      // Create destination directory if needed
      if (options?.createDir) {
        const destDir = path.dirname(destPath);
        if (!fs.existsSync(destDir)) {
          fs.mkdirSync(destDir, { recursive: true });
        }
      }

      fs.copyFileSync(sourcePath, destPath);
      return {
        success: true,
        message: `Successfully copied file from ${sourcePath} to ${destPath}`,
        data: { source: sourcePath, destination: destPath }
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to copy file: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Move/rename a file
   */
  public static moveFile(sourcePath: string, destPath: string, options?: { createDir?: boolean }): FileOperation {
    try {
      if (!fs.existsSync(sourcePath)) {
        return {
          success: false,
          message: `Source file not found: ${sourcePath}`
        };
      }

      // Create destination directory if needed
      if (options?.createDir) {
        const destDir = path.dirname(destPath);
        if (!fs.existsSync(destDir)) {
          fs.mkdirSync(destDir, { recursive: true });
        }
      }

      fs.renameSync(sourcePath, destPath);
      return {
        success: true,
        message: `Successfully moved file from ${sourcePath} to ${destPath}`,
        data: { source: sourcePath, destination: destPath }
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to move file: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Search for files matching a pattern
   */
  public static searchFiles(dirPath: string, pattern: string | RegExp): FileOperation {
    try {
      if (!fs.existsSync(dirPath)) {
        return {
          success: false,
          message: `Directory not found: ${dirPath}`
        };
      }

      const searchPattern = typeof pattern === 'string' ? new RegExp(pattern) : pattern;
      const matches: string[] = [];

      const searchRecursive = (currentPath: string) => {
        const items = fs.readdirSync(currentPath);
        
        for (const item of items) {
          const itemPath = path.join(currentPath, item);
          const stats = fs.statSync(itemPath);
          
          if (stats.isFile() && searchPattern.test(item)) {
            matches.push(itemPath);
          } else if (stats.isDirectory()) {
            searchRecursive(itemPath);
          }
        }
      };

      searchRecursive(dirPath);

      return {
        success: true,
        message: `Search completed in: ${dirPath}`,
        data: {
          pattern: pattern.toString(),
          matches,
          count: matches.length
        }
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to search files: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }
}