# Patent Search System - Architecture Documentation

## System Architecture

### Overview
The Patent Search System is a 3-tier desktop application built on .NET Framework 4.5, following traditional layered architecture patterns common in enterprise Windows applications of 2014.

### Architecture Layers

#### 1. Presentation Layer (Windows Forms)
- **Main Form**: Container with menu, toolbar, and status bar
- **Search Panel**: Multi-criteria search controls
- **Data Grid**: Patent list display with sorting and pagination
- **Detail View**: Patent information editing form
- **Import/Export Dialogs**: Excel file handling interfaces

#### 2. Business Logic Layer
- **PatentService**: Core patent CRUD operations
- **SearchService**: Full-text search and filtering logic
- **ExcelService**: Import/export business rules
- **UserService**: Authentication and authorization
- **FileService**: Document attachment management

#### 3. Data Access Layer
- **PatentRepository**: SQL Server data access via ADO.NET
- **SearchIndex**: Lucene.NET index management
- **FileRepository**: File system operations
- **CacheManager**: SQLite local caching

### Database Schema

```sql
-- Core patent table
CREATE TABLE Patents (
    PatentID INT PRIMARY KEY IDENTITY,
    PatentNumber NVARCHAR(50) NOT NULL,
    Title NVARCHAR(500) NOT NULL,
    Abstract NVARCHAR(MAX),
    Claims NVARCHAR(MAX),
    Inventor NVARCHAR(200),
    Assignee NVARCHAR(200),
    FilingDate DATE,
    PublicationDate DATE,
    PatentType NVARCHAR(50),
    Status NVARCHAR(50),
    CreatedDate DATETIME DEFAULT GETDATE(),
    ModifiedDate DATETIME
);

-- Full-text search catalog
CREATE FULLTEXT CATALOG PatentCatalog AS DEFAULT;

CREATE FULLTEXT INDEX ON Patents(Title, Abstract, Claims)
KEY INDEX PK_Patents
ON PatentCatalog;

-- Document attachments
CREATE TABLE PatentDocuments (
    DocumentID INT PRIMARY KEY IDENTITY,
    PatentID INT FOREIGN KEY REFERENCES Patents(PatentID),
    FileName NVARCHAR(255),
    FilePath NVARCHAR(500),
    FileType NVARCHAR(50),
    UploadDate DATETIME DEFAULT GETDATE()
);

-- User management
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY,
    UserName NVARCHAR(50) NOT NULL,
    PasswordHash NVARCHAR(255) NOT NULL,
    Role NVARCHAR(50) DEFAULT 'User',
    IsActive BIT DEFAULT 1
);

-- Search history
CREATE TABLE SearchHistory (
    HistoryID INT PRIMARY KEY IDENTITY,
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    QueryText NVARCHAR(500),
    SearchDate DATETIME DEFAULT GETDATE()
);
```

### Search Implementation

#### Lucene.NET Index Structure
```csharp
public void IndexPatent(Patent patent)
{
    var document = new Document();
    
    // Stored fields (retrievable)
    document.Add(new Field("PatentID", patent.PatentID.ToString(), 
        Field.Store.YES, Field.Index.NO));
    document.Add(new Field("PatentNumber", patent.PatentNumber, 
        Field.Store.YES, Field.Index.NO));
    
    // Indexed fields (searchable)
    document.Add(new Field("Title", patent.Title, 
        Field.Store.YES, Field.Index.ANALYZED));
    document.Add(new Field("Abstract", patent.Abstract, 
        Field.Store.YES, Field.Index.ANALYZED));
    document.Add(new Field("Claims", patent.Claims, 
        Field.Store.YES, Field.Index.ANALYZED));
    document.Add(new Field("Inventor", patent.Inventor, 
        Field.Store.YES, Field.Index.ANALYZED));
    
    // Facet fields (filterable)
    document.Add(new Field("FilingYear", patent.FilingDate.Year.ToString(), 
        Field.Store.NO, Field.Index.NOT_ANALYZED));
    document.Add(new Field("PatentType", patent.PatentType, 
        Field.Store.NO, Field.Index.NOT_ANALYZED));
    
    writer.AddDocument(document);
}
```

### Performance Optimizations

1. **Database Indexing**
   - Clustered index on PatentID
   - Non-clustered indexes on PatentNumber, FilingDate
   - Full-text index on Title, Abstract, Claims

2. **Caching Strategy**
   - SQLite local cache for frequently accessed patents
   - In-memory cache for search suggestions
   - File system cache for document previews

3. **Search Optimization**
   - Lucene.NET index segmentation
   - Query result pagination (50 records per page)
   - Background index updates

### Security Considerations

1. **Data Protection**
   - SQL injection prevention via parameterized queries
   - XSS prevention in patent text display
   - File upload validation and sandboxing

2. **Access Control**
   - Password hashing with SHA256
   - Role-based permissions (Admin, User, Viewer)
   - Audit logging for data modifications

3. **Backup Strategy**
   - Automated daily SQL Server backups
   - Lucene index replication
   - Document file system backup

---

*Architecture documentation for the Patent Search System (2014)*
