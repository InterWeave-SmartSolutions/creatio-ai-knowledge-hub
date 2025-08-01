/**
 * Test data generation utilities for JavaScript/TypeScript tests
 */
import { faker } from '@faker-js/faker';
import fs from 'fs/promises';
import path from 'path';

export interface VideoContent {
  id: string;
  title: string;
  filePath: string;
  duration: number;
  transcript: string;
  summary: string;
  topics: string[];
  complexityLevel: 'beginner' | 'intermediate' | 'advanced';
  commands: string[];
  apiReferences: string[];
  codeExamples: CodeExample[];
  createdAt: Date;
}

export interface PDFContent {
  id: string;
  title: string;
  filePath: string;
  pageCount: number;
  content: string;
  sections: PDFSection[];
  topics: string[];
  commands: string[];
  apiReferences: string[];
  codeExamples: CodeExample[];
  createdAt: Date;
}

export interface CodeExample {
  language: string;
  code: string;
  description: string;
}

export interface PDFSection {
  title: string;
  content: string;
  pageNumber: number;
}

export interface Command {
  id: number;
  command: string;
  description: string;
  category: string;
  parameters: string[];
}

export class TestDataGenerator {
  private static readonly TOPICS = [
    'creatio', 'bpm', 'crm', 'development', 'javascript', 'c#', 'configuration',
    'api', 'documentation', 'architecture', 'integration', 'workflow'
  ];

  private static readonly COMMANDS = [
    'CreateSection', 'AddField', 'ConfigureProcess', 'SetupIntegration',
    'CreateEntity', 'ModifySchema', 'AddBusinessRule', 'CreateLookup',
    'DefinePermissions', 'ConfigureUI', 'SetupValidation', 'CreateReport'
  ];

  private static readonly API_REFERENCES = [
    'EntitySchema', 'UserConnection', 'ProcessSchema', 'ServiceApi',
    'ConfigurationService', 'MessagePublisher', 'EntitySchemaManager',
    'ProcessFlowElementSchema', 'SysSettings', 'GlobalSearch'
  ];

  private static readonly CATEGORIES = [
    'UI', 'Business Logic', 'Integration', 'Configuration', 'Data',
    'Security', 'Reporting', 'Workflow', 'API', 'System'
  ];

  /**
   * Generate a single video content object
   */
  static generateVideoContent(overrides: Partial<VideoContent> = {}): VideoContent {
    const id = faker.string.uuid();
    const topics = faker.helpers.arrayElements(this.TOPICS, { min: 2, max: 5 });
    const commands = faker.helpers.arrayElements(this.COMMANDS, { min: 1, max: 4 });
    const apiReferences = faker.helpers.arrayElements(this.API_REFERENCES, { min: 1, max: 3 });

    return {
      id,
      title: faker.lorem.words({ min: 3, max: 6 }),
      filePath: `/videos/${id}.mp4`,
      duration: faker.number.float({ min: 30, max: 1800 }),
      transcript: faker.lorem.paragraph({ min: 10, max: 20 }),
      summary: faker.lorem.paragraph({ min: 2, max: 4 }),
      topics,
      complexityLevel: faker.helpers.arrayElement(['beginner', 'intermediate', 'advanced']),
      commands,
      apiReferences,
      codeExamples: this.generateCodeExamples(),
      createdAt: faker.date.past({ years: 1 }),
      ...overrides,
    };
  }

  /**
   * Generate multiple video content objects
   */
  static generateVideoContents(count: number): VideoContent[] {
    return Array.from({ length: count }, () => this.generateVideoContent());
  }

  /**
   * Generate a single PDF content object
   */
  static generatePDFContent(overrides: Partial<PDFContent> = {}): PDFContent {
    const id = faker.string.uuid();
    const pageCount = faker.number.int({ min: 5, max: 50 });
    const topics = faker.helpers.arrayElements(this.TOPICS, { min: 2, max: 4 });

    return {
      id,
      title: faker.lorem.words({ min: 4, max: 8 }),
      filePath: `/pdfs/${id}.pdf`,
      pageCount,
      content: faker.lorem.paragraphs({ min: 10, max: 30 }),
      sections: this.generatePDFSections(pageCount),
      topics,
      commands: [],
      apiReferences: [],
      codeExamples: [],
      createdAt: faker.date.past({ years: 1 }),
      ...overrides,
    };
  }

  /**
   * Generate multiple PDF content objects
   */
  static generatePDFContents(count: number): PDFContent[] {
    return Array.from({ length: count }, () => this.generatePDFContent());
  }

  /**
   * Generate a single command object
   */
  static generateCommand(overrides: Partial<Command> = {}): Command {
    return {
      id: faker.number.int({ min: 1, max: 10000 }),
      command: faker.helpers.arrayElement(this.COMMANDS),
      description: faker.lorem.sentence(),
      category: faker.helpers.arrayElement(this.CATEGORIES),
      parameters: faker.helpers.arrayElements(
        ['name', 'value', 'type', 'required', 'default'],
        { min: 0, max: 3 }
      ),
      ...overrides,
    };
  }

  /**
   * Generate multiple command objects
   */
  static generateCommands(count: number): Command[] {
    return Array.from({ length: count }, () => this.generateCommand());
  }

  /**
   * Generate code examples
   */
  private static generateCodeExamples(): CodeExample[] {
    const languages = ['javascript', 'csharp', 'sql'];
    const selectedLanguages = faker.helpers.arrayElements(languages, { min: 1, max: 2 });
    
    return selectedLanguages.map(lang => ({
      language: lang,
      code: this.generateCodeForLanguage(lang),
      description: faker.lorem.sentence(),
    }));
  }

  /**
   * Generate code for specific language
   */
  private static generateCodeForLanguage(language: string): string {
    switch (language) {
      case 'javascript':
        return `var schema = this.Ext.create('EntitySchema', {
    name: '${faker.lorem.word()}',
    columns: {
        '${faker.lorem.word()}': {
            dataValueType: Terrasoft.DataValueType.TEXT
        }
    }
});`;
      case 'csharp':
        return `var entity = UserConnection.EntitySchemaManager.GetInstanceByName('${faker.lorem.word()}');
var query = new EntitySchemaQuery(entity);
query.AddAllSchemaColumns();
var result = query.GetEntityCollection(UserConnection);`;
      case 'sql':
        return `SELECT Id, Name, CreatedOn 
FROM ${faker.lorem.word()} 
WHERE CreatedOn > @StartDate 
ORDER BY CreatedOn DESC`;
      default:
        return faker.lorem.paragraph();
    }
  }

  /**
   * Generate PDF sections
   */
  private static generatePDFSections(pageCount: number): PDFSection[] {
    const sectionCount = faker.number.int({ min: 3, max: 8 });
    return Array.from({ length: sectionCount }, () => ({
      title: faker.lorem.words({ min: 2, max: 5 }),
      content: faker.lorem.paragraphs({ min: 3, max: 7 }),
      pageNumber: faker.number.int({ min: 1, max: pageCount }),
    }));
  }

  /**
   * Generate complete test dataset
   */
  static generateTestDataset(options: {
    videoCount?: number;
    pdfCount?: number;
    commandCount?: number;
  } = {}): {
    videos: VideoContent[];
    pdfs: PDFContent[];
    commands: Command[];
    metadata: {
      generatedAt: string;
      videoCount: number;
      pdfCount: number;
      commandCount: number;
    };
  } {
    const {
      videoCount = 50,
      pdfCount = 30,
      commandCount = 20,
    } = options;

    const videos = this.generateVideoContents(videoCount);
    const pdfs = this.generatePDFContents(pdfCount);
    const commands = this.generateCommands(commandCount);

    return {
      videos,
      pdfs,
      commands,
      metadata: {
        generatedAt: new Date().toISOString(),
        videoCount: videos.length,
        pdfCount: pdfs.length,
        commandCount: commands.length,
      },
    };
  }

  /**
   * Save test dataset to file
   */
  static async saveTestDataset(
    filePath: string,
    options: Parameters<typeof TestDataGenerator.generateTestDataset>[0] = {}
  ): Promise<void> {
    const dataset = this.generateTestDataset(options);
    const dir = path.dirname(filePath);
    
    await fs.mkdir(dir, { recursive: true });
    await fs.writeFile(filePath, JSON.stringify(dataset, null, 2));
  }

  /**
   * Load test dataset from file
   */
  static async loadTestDataset(filePath: string): Promise<ReturnType<typeof TestDataGenerator.generateTestDataset>> {
    const content = await fs.readFile(filePath, 'utf-8');
    return JSON.parse(content);
  }

  /**
   * Generate minimal test data for unit tests
   */
  static generateMinimalTestData(): {
    video: VideoContent;
    pdf: PDFContent;
    command: Command;
  } {
    return {
      video: this.generateVideoContent(),
      pdf: this.generatePDFContent(),
      command: this.generateCommand(),
    };
  }
}

// CLI interface for generating test data
if (require.main === module) {
  const outputPath = path.join(__dirname, 'test-data.json');
  
  TestDataGenerator.saveTestDataset(outputPath, {
    videoCount: 100,
    pdfCount: 50,
    commandCount: 30,
  })
    .then(() => {
      console.log(`Test data generated and saved to ${outputPath}`);
    })
    .catch((error) => {
      console.error('Error generating test data:', error);
      process.exit(1);
    });
}
