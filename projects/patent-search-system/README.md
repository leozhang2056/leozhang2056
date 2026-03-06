# Patent Search System

**.NET 2.0 Desktop Application for Patent Document Management**

A comprehensive Windows desktop application developed in 2014 using **.NET Framework 2.0** and **C# 3.0**. 
This enterprise system showcases early adoption of Microsoft technology stack, featuring Windows Forms 2.0 UI, 
SQL Server 2008 database, Lucene.NET 2.9 full-text search, and advanced Excel data processing capabilities.

> **Tech Stack Highlight:** .NET Framework 2.0 | C# 3.0 | Windows Forms 2.0 | SQL Server 2008 | Lucene.NET 2.9 | ADO.NET 2.0

---

## 🎯 Project Overview

This system was designed to help research teams efficiently manage large volumes of patent documents, enabling quick search and retrieval of patent information through an intuitive desktop interface.

**Key Capabilities:**
- Patent document CRUD operations
- Excel batch import/export with data validation
- Full-text search across patent metadata
- Multi-criteria advanced search
- Document attachment management
- User authentication and role-based access

---

## 🛠️ .NET 2.0 Technology Stack

| Layer | Technologies |
|-------|-------------|
| **.NET Framework** | .NET Framework 2.0, CLR 2.0, BCL 2.0 |
| **Language** | C# 3.0, LINQ (via LINQBridge), Generics |
| **Desktop UI** | Windows Forms 2.0, Data Binding, GDI+ |
| **Data Access** | ADO.NET 2.0, SQL Server 2008, SQLite 3 |
| **Search Engine** | Lucene.NET 2.9 (full-text indexing) |
| **Office Integration** | EPPlus (Excel 2007+), iTextSharp (PDF) |
| **Development Tools** | Visual Studio 2008, SQL Server Management Studio 2008 |
| **Patterns** | 3-Tier Architecture, Repository Pattern, Provider Pattern |

---

## ✨ Key Features

### 1. Excel Import/Export
- Batch import patent data from Excel files
- Data validation and error reporting
- Export search results to Excel
- Template-based data entry

### 2. Full-Text Search
- **Lucene.NET** powered search engine
- Search across patent titles, abstracts, and claims
- Sub-second search response time (<2s)
- Search history and favorites

### 3. Advanced Filtering
- Multi-criteria search:
  - Patent number
  - Title keywords
  - Inventor name
  - Filing date range
  - Patent category
  - Status

### 4. Document Management
- Attach PDF and image files to patent records
- File system integration
- Document preview
- Version control

### 5. User Management
- Role-based access control
- User authentication
- Audit logging
- Data backup and restore

---

## 📊 System Metrics

| Metric | Value |
|--------|-------|
| Patent Records Managed | 10,000+ |
| Search Response Time | <2 seconds |
| Daily Active Users | 50+ |
| Uptime | 99.5% |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│         Windows Forms UI            │
│  ┌─────────┐ ┌─────────────────┐   │
│  │ Search  │ │  Data Grid View │   │
│  │ Panel   │ │                 │   │
│  └─────────┘ └─────────────────┘   │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│       Business Logic Layer          │
│  ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │  Patent │ │  Search │ │  Excel ││
│  │ Service │ │ Service │ │ Service││
│  └─────────┘ └─────────┘ └────────┘│
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│       Data Access Layer             │
│  ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │ADO.NET  │ │Lucene.NET│ │ File ││
│  │ SQL Svr │ │  Index   │ │System││
│  └─────────┘ └─────────┘ └────────┘│
└─────────────────────────────────────┘
```

---

## 💡 Technical Highlights

### Full-Text Search Implementation
```csharp
// Lucene.NET integration for patent search
using Lucene.Net.Analysis.Standard;
using Lucene.Net.Documents;
using Lucene.Net.Index;
using Lucene.Net.Search;

public List<Patent> SearchPatents(string query, SearchFilter filter)
{
    using (var searcher = new IndexSearcher(directory))
    {
        var analyzer = new StandardAnalyzer();
        var queryParser = new MultiFieldQueryParser(
            Lucene.Net.Util.Version.LUCENE_30,
            new[] { "Title", "Abstract", "Claims" },
            analyzer);
        
        var luceneQuery = queryParser.Parse(query);
        var hits = searcher.Search(luceneQuery, filter.MaxResults);
        
        return MapToPatentList(hits);
    }
}
```

### Excel Data Processing
```csharp
// EPPlus for Excel import/export
using OfficeOpenXml;

public void ExportToExcel(List<Patent> patents, string filePath)
{
    using (var package = new ExcelPackage())
    {
        var worksheet = package.Workbook.Worksheets.Add("Patents");
        
        // Headers
        worksheet.Cells[1, 1].Value = "Patent Number";
        worksheet.Cells[1, 2].Value = "Title";
        worksheet.Cells[1, 3].Value = "Inventor";
        worksheet.Cells[1, 4].Value = "Filing Date";
        
        // Data
        for (int i = 0; i < patents.Count; i++)
        {
            worksheet.Cells[i + 2, 1].Value = patents[i].PatentNumber;
            worksheet.Cells[i + 2, 2].Value = patents[i].Title;
            worksheet.Cells[i + 2, 3].Value = patents[i].Inventor;
            worksheet.Cells[i + 2, 4].Value = patents[i].FilingDate;
        }
        
        package.SaveAs(new FileInfo(filePath));
    }
}
```

---

## 📁 Project Structure

```
patent-search-system/
├── README.md              # This file
├── facts.yaml             # Structured project data for AI/KB
├── docs/                  # Documentation (if available)
│   ├── architecture.md
│   └── user-manual.md
└── images/                # Screenshots (if available)
    ├── main-interface.png
    ├── search-results.png
    └── excel-export.png
```

---

## 🎓 Learning Outcomes

This early-career project provided foundational experience in:

1. **Desktop Application Development**
   - Windows Forms UI design patterns
   - Event-driven programming
   - Data binding and validation

2. **Database Design**
   - SQL Server schema design
   - Indexing strategies for search performance
   - Transaction management

3. **Search Technology**
   - Full-text search implementation
   - Lucene.NET indexing and querying
   - Search relevance tuning

4. **Data Processing**
   - Excel file manipulation
   - Batch data import/export
   - Data validation and cleansing

---

## 🔗 Related Projects

This project laid the foundation for subsequent enterprise development work:

- **[Enterprise Messaging](../enterprise-messaging/)** — Evolved from .NET desktop to Java backend
- **[Smart Factory](../smart-factory/)** — Applied database design skills to larger scale systems

---

## 📅 Timeline

- **Development Period:** 2014 (6 months)
- **Team Size:** 2 developers
- **Status:** Deployed and actively used by research team

---

*Part of the Career Knowledge Base project — structured data for AI-powered resume generation.*
