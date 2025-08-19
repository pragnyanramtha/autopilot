import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { APProfile } from '../setup/InitWizard.js';

export class ProfileManager {
  private static instance: ProfileManager;
  private profilePath: string;
  private profile: APProfile | null = null;

  private constructor() {
    this.profilePath = path.join(os.homedir(), '.ap', 'profile.json');
  }

  public static getInstance(): ProfileManager {
    if (!ProfileManager.instance) {
      ProfileManager.instance = new ProfileManager();
    }
    return ProfileManager.instance;
  }

  public async loadProfile(): Promise<APProfile | null> {
    if (this.profile) {
      return this.profile;
    }

    try {
      if (fs.existsSync(this.profilePath)) {
        const profileData = fs.readFileSync(this.profilePath, 'utf8');
        this.profile = JSON.parse(profileData);
        return this.profile;
      }
    } catch (error) {
      console.warn('⚠️  Could not load user profile:', error);
    }

    return null;
  }

  public async getAIContext(): Promise<string> {
    const profile = await this.loadProfile();
    
    if (!profile) {
      return `User Profile: Not initialized. Please run "ap init" to set up personalized assistance.
System: Linux (architecture unknown)
Default behavior: Use conservative automation and provide detailed explanations.`;
    }

    return profile.ai_context;
  }

  public async getUserName(): Promise<string> {
    const profile = await this.loadProfile();
    return profile?.user_preferences.preferred_name || 'user';
  }

  public async getPreferredPackageManager(): Promise<string> {
    const profile = await this.loadProfile();
    return profile?.user_preferences.package_manager_preference[0] || 'apt';
  }

  public async getPreferredEditor(): Promise<string> {
    const profile = await this.loadProfile();
    return profile?.user_preferences.text_editor || 'nano';
  }

  public async getPreferredCodeEditor(): Promise<string> {
    const profile = await this.loadProfile();
    return profile?.user_preferences.code_editor || 'vscode';
  }

  public async getSystemInfo(): Promise<any> {
    const profile = await this.loadProfile();
    return profile?.system_info || null;
  }

  public async isInitialized(): Promise<boolean> {
    return fs.existsSync(this.profilePath);
  }

  public async updateProfile(updates: Partial<APProfile>): Promise<void> {
    const profile = await this.loadProfile();
    if (profile) {
      const updatedProfile = { ...profile, ...updates, updated_at: new Date().toISOString() };
      fs.writeFileSync(this.profilePath, JSON.stringify(updatedProfile, null, 2));
      this.profile = updatedProfile;
    }
  }

  public getProfilePath(): string {
    return this.profilePath;
  }
}