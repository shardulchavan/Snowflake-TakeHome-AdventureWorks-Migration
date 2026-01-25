-- =============================================
-- Table Creation
-- =============================================

-- Table: DBO.AWBuildVersion (1 rows)
CREATE TABLE IF NOT EXISTS DBO.AWBuildVersion (
    SystemInformationID NUMBER(38,0) DEFAULT DBO.DBO_AWBUILDVERSION_SYSTEMINFORMATIONID_SEQ.NEXTVAL NOT NULL,
    "Database Version" VARCHAR(25) NOT NULL,
    VersionDate TIMESTAMP_NTZ NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: DBO.DatabaseLog (1,596 rows)
CREATE TABLE IF NOT EXISTS DBO.DatabaseLog (
    DatabaseLogID NUMBER(38,0) DEFAULT DBO.DBO_DATABASELOG_DATABASELOGID_SEQ.NEXTVAL NOT NULL,
    PostTime TIMESTAMP_NTZ NOT NULL,
    DatabaseUser VARCHAR(16777216) NOT NULL,
    Event VARCHAR(16777216) NOT NULL,
    "Schema" VARCHAR(16777216) NULL,
    Object VARCHAR(16777216) NULL,
    TSQL VARCHAR(16777216) NOT NULL,
    XmlEvent VARCHAR(16777216) NOT NULL
);

-- Table: DBO.ErrorLog (0 rows)
CREATE TABLE IF NOT EXISTS DBO.ErrorLog (
    ErrorLogID NUMBER(38,0) DEFAULT DBO.DBO_ERRORLOG_ERRORLOGID_SEQ.NEXTVAL NOT NULL,
    ErrorTime TIMESTAMP_NTZ NOT NULL,
    UserName VARCHAR(16777216) NOT NULL,
    ErrorNumber NUMBER(38,0) NOT NULL,
    ErrorSeverity NUMBER(38,0) NULL,
    ErrorState NUMBER(38,0) NULL,
    ErrorProcedure VARCHAR(126) NULL,
    ErrorLine NUMBER(38,0) NULL,
    ErrorMessage VARCHAR(4000) NOT NULL
);

-- Table: Humanresources.Department (16 rows)
CREATE TABLE IF NOT EXISTS Humanresources.Department (
    DepartmentID NUMBER(38,0) DEFAULT Humanresources.HUMANRESOURCES_DEPARTMENT_DEPARTMENTID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    GroupName VARCHAR(16777216) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Humanresources.Employee (290 rows)
CREATE TABLE IF NOT EXISTS Humanresources.Employee (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    NationalIDNumber VARCHAR(15) NOT NULL,
    LoginID VARCHAR(256) NOT NULL,
    OrganizationNode VARCHAR(4000) NULL,
    OrganizationLevel NUMBER(38,0) NULL,
    JobTitle VARCHAR(50) NOT NULL,
    BirthDate DATE NOT NULL,
    MaritalStatus CHAR(1) NOT NULL,
    Gender CHAR(1) NOT NULL,
    HireDate DATE NOT NULL,
    SalariedFlag VARCHAR(16777216) NOT NULL,
    VacationHours NUMBER(38,0) NOT NULL,
    SickLeaveHours NUMBER(38,0) NOT NULL,
    CurrentFlag VARCHAR(16777216) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Humanresources.EmployeeDepartmentHistory (296 rows)
CREATE TABLE IF NOT EXISTS Humanresources.EmployeeDepartmentHistory (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    DepartmentID NUMBER(38,0) NOT NULL,
    ShiftID NUMBER(38,0) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Humanresources.EmployeePayHistory (316 rows)
CREATE TABLE IF NOT EXISTS Humanresources.EmployeePayHistory (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    RateChangeDate TIMESTAMP_NTZ NOT NULL,
    Rate NUMBER(19,4) NOT NULL,
    PayFrequency NUMBER(38,0) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Humanresources.JobCandidate (13 rows)
CREATE TABLE IF NOT EXISTS Humanresources.JobCandidate (
    JobCandidateID NUMBER(38,0) DEFAULT Humanresources.HUMANRESOURCES_JOBCANDIDATE_JOBCANDIDATEID_SEQ.NEXTVAL NOT NULL,
    BusinessEntityID NUMBER(38,0) NULL,
    Resume VARCHAR(16777216) NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Humanresources.Shift (3 rows)
CREATE TABLE IF NOT EXISTS Humanresources.Shift (
    ShiftID NUMBER(38,0) DEFAULT Humanresources.HUMANRESOURCES_SHIFT_SHIFTID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.Address (19,614 rows)
CREATE TABLE IF NOT EXISTS Person.Address (
    AddressID NUMBER(38,0) DEFAULT Person.PERSON_ADDRESS_ADDRESSID_SEQ.NEXTVAL NOT NULL,
    AddressLine1 VARCHAR(60) NOT NULL,
    AddressLine2 VARCHAR(60) NULL,
    City VARCHAR(30) NOT NULL,
    StateProvinceID NUMBER(38,0) NOT NULL,
    PostalCode VARCHAR(15) NOT NULL,
    SpatialLocation GEOGRAPHY NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.AddressType (6 rows)
CREATE TABLE IF NOT EXISTS Person.AddressType (
    AddressTypeID NUMBER(38,0) DEFAULT Person.PERSON_ADDRESSTYPE_ADDRESSTYPEID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.BusinessEntity (20,777 rows)
CREATE TABLE IF NOT EXISTS Person.BusinessEntity (
    BusinessEntityID NUMBER(38,0) DEFAULT Person.PERSON_BUSINESSENTITY_BUSINESSENTITYID_SEQ.NEXTVAL NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.BusinessEntityAddress (19,614 rows)
CREATE TABLE IF NOT EXISTS Person.BusinessEntityAddress (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    AddressID NUMBER(38,0) NOT NULL,
    AddressTypeID NUMBER(38,0) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.BusinessEntityContact (909 rows)
CREATE TABLE IF NOT EXISTS Person.BusinessEntityContact (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    PersonID NUMBER(38,0) NOT NULL,
    ContactTypeID NUMBER(38,0) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.ContactType (20 rows)
CREATE TABLE IF NOT EXISTS Person.ContactType (
    ContactTypeID NUMBER(38,0) DEFAULT Person.PERSON_CONTACTTYPE_CONTACTTYPEID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.CountryRegion (238 rows)
CREATE TABLE IF NOT EXISTS Person.CountryRegion (
    CountryRegionCode VARCHAR(3) NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.EmailAddress (19,972 rows)
CREATE TABLE IF NOT EXISTS Person.EmailAddress (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    EmailAddressID NUMBER(38,0) DEFAULT Person.PERSON_EMAILADDRESS_EMAILADDRESSID_SEQ.NEXTVAL NOT NULL,
    EmailAddress VARCHAR(50) NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.Password (19,972 rows)
CREATE TABLE IF NOT EXISTS Person.Password (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    PasswordHash VARCHAR(128) NOT NULL,
    PasswordSalt VARCHAR(10) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.Person (19,972 rows)
CREATE TABLE IF NOT EXISTS Person.Person (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    PersonType CHAR(2) NOT NULL,
    NameStyle VARCHAR(16777216) NOT NULL,
    Title VARCHAR(8) NULL,
    FirstName VARCHAR(16777216) NOT NULL,
    MiddleName VARCHAR(16777216) NULL,
    LastName VARCHAR(16777216) NOT NULL,
    Suffix VARCHAR(10) NULL,
    EmailPromotion NUMBER(38,0) NOT NULL,
    AdditionalContactInfo VARCHAR(16777216) NULL,
    Demographics VARCHAR(16777216) NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.PersonPhone (19,972 rows)
CREATE TABLE IF NOT EXISTS Person.PersonPhone (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    PhoneNumber VARCHAR(16777216) NOT NULL,
    PhoneNumberTypeID NUMBER(38,0) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.PhoneNumberType (3 rows)
CREATE TABLE IF NOT EXISTS Person.PhoneNumberType (
    PhoneNumberTypeID NUMBER(38,0) DEFAULT Person.PERSON_PHONENUMBERTYPE_PHONENUMBERTYPEID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Person.StateProvince (181 rows)
CREATE TABLE IF NOT EXISTS Person.StateProvince (
    StateProvinceID NUMBER(38,0) DEFAULT Person.PERSON_STATEPROVINCE_STATEPROVINCEID_SEQ.NEXTVAL NOT NULL,
    StateProvinceCode CHAR(3) NOT NULL,
    CountryRegionCode VARCHAR(3) NOT NULL,
    IsOnlyStateProvinceFlag VARCHAR(16777216) NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    TerritoryID NUMBER(38,0) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.BillOfMaterials (2,679 rows)
CREATE TABLE IF NOT EXISTS Production.BillOfMaterials (
    BillOfMaterialsID NUMBER(38,0) DEFAULT Production.PRODUCTION_BILLOFMATERIALS_BILLOFMATERIALSID_SEQ.NEXTVAL NOT NULL,
    ProductAssemblyID NUMBER(38,0) NULL,
    ComponentID NUMBER(38,0) NOT NULL,
    StartDate TIMESTAMP_NTZ NOT NULL,
    EndDate TIMESTAMP_NTZ NULL,
    UnitMeasureCode CHAR(3) NOT NULL,
    BOMLevel NUMBER(38,0) NOT NULL,
    PerAssemblyQty NUMBER(8,2) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.Culture (8 rows)
CREATE TABLE IF NOT EXISTS Production.Culture (
    CultureID CHAR(6) NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.Document (13 rows)
CREATE TABLE IF NOT EXISTS Production.Document (
    DocumentNode VARCHAR(4000) NOT NULL,
    DocumentLevel NUMBER(38,0) NULL,
    Title VARCHAR(50) NOT NULL,
    Owner NUMBER(38,0) NOT NULL,
    FolderFlag BOOLEAN NOT NULL,
    FileName VARCHAR(400) NOT NULL,
    FileExtension VARCHAR(8) NOT NULL,
    Revision CHAR(5) NOT NULL,
    ChangeNumber NUMBER(38,0) NOT NULL,
    Status NUMBER(38,0) NOT NULL,
    DocumentSummary VARCHAR(16777216) NULL,
    Document BINARY(16777216) NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.Illustration (5 rows)
CREATE TABLE IF NOT EXISTS Production.Illustration (
    IllustrationID NUMBER(38,0) DEFAULT Production.PRODUCTION_ILLUSTRATION_ILLUSTRATIONID_SEQ.NEXTVAL NOT NULL,
    Diagram VARCHAR(16777216) NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.Location (14 rows)
CREATE TABLE IF NOT EXISTS Production.Location (
    LocationID NUMBER(38,0) DEFAULT Production.PRODUCTION_LOCATION_LOCATIONID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    CostRate NUMBER(10,4) NOT NULL,
    Availability NUMBER(8,2) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.Product (504 rows)
CREATE TABLE IF NOT EXISTS Production.Product (
    ProductID NUMBER(38,0) DEFAULT Production.PRODUCTION_PRODUCT_PRODUCTID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    ProductNumber VARCHAR(25) NOT NULL,
    MakeFlag VARCHAR(16777216) NOT NULL,
    FinishedGoodsFlag VARCHAR(16777216) NOT NULL,
    Color VARCHAR(15) NULL,
    SafetyStockLevel NUMBER(38,0) NOT NULL,
    ReorderPoint NUMBER(38,0) NOT NULL,
    StandardCost NUMBER(19,4) NOT NULL,
    ListPrice NUMBER(19,4) NOT NULL,
    Size VARCHAR(5) NULL,
    SizeUnitMeasureCode CHAR(3) NULL,
    WeightUnitMeasureCode CHAR(3) NULL,
    Weight NUMBER(8,2) NULL,
    DaysToManufacture NUMBER(38,0) NOT NULL,
    ProductLine CHAR(2) NULL,
    Class CHAR(2) NULL,
    Style CHAR(2) NULL,
    ProductSubcategoryID NUMBER(38,0) NULL,
    ProductModelID NUMBER(38,0) NULL,
    SellStartDate TIMESTAMP_NTZ NOT NULL,
    SellEndDate TIMESTAMP_NTZ NULL,
    DiscontinuedDate TIMESTAMP_NTZ NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductCategory (4 rows)
CREATE TABLE IF NOT EXISTS Production.ProductCategory (
    ProductCategoryID NUMBER(38,0) DEFAULT Production.PRODUCTION_PRODUCTCATEGORY_PRODUCTCATEGORYID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductCostHistory (395 rows)
CREATE TABLE IF NOT EXISTS Production.ProductCostHistory (
    ProductID NUMBER(38,0) NOT NULL,
    StartDate TIMESTAMP_NTZ NOT NULL,
    EndDate TIMESTAMP_NTZ NULL,
    StandardCost NUMBER(19,4) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductDescription (762 rows)
CREATE TABLE IF NOT EXISTS Production.ProductDescription (
    ProductDescriptionID NUMBER(38,0) DEFAULT Production.PRODUCTION_PRODUCTDESCRIPTION_PRODUCTDESCRIPTIONID_SEQ.NEXTVAL NOT NULL,
    Description VARCHAR(400) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductDocument (32 rows)
CREATE TABLE IF NOT EXISTS Production.ProductDocument (
    ProductID NUMBER(38,0) NOT NULL,
    DocumentNode VARCHAR(4000) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductInventory (1,069 rows)
CREATE TABLE IF NOT EXISTS Production.ProductInventory (
    ProductID NUMBER(38,0) NOT NULL,
    LocationID NUMBER(38,0) NOT NULL,
    Shelf VARCHAR(10) NOT NULL,
    Bin NUMBER(38,0) NOT NULL,
    Quantity NUMBER(38,0) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductListPriceHistory (395 rows)
CREATE TABLE IF NOT EXISTS Production.ProductListPriceHistory (
    ProductID NUMBER(38,0) NOT NULL,
    StartDate TIMESTAMP_NTZ NOT NULL,
    EndDate TIMESTAMP_NTZ NULL,
    ListPrice NUMBER(19,4) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductModel (128 rows)
CREATE TABLE IF NOT EXISTS Production.ProductModel (
    ProductModelID NUMBER(38,0) DEFAULT Production.PRODUCTION_PRODUCTMODEL_PRODUCTMODELID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    CatalogDescription VARCHAR(16777216) NULL,
    Instructions VARCHAR(16777216) NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductModelIllustration (7 rows)
CREATE TABLE IF NOT EXISTS Production.ProductModelIllustration (
    ProductModelID NUMBER(38,0) NOT NULL,
    IllustrationID NUMBER(38,0) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductModelProductDescriptionCulture (762 rows)
CREATE TABLE IF NOT EXISTS Production.ProductModelProductDescriptionCulture (
    ProductModelID NUMBER(38,0) NOT NULL,
    ProductDescriptionID NUMBER(38,0) NOT NULL,
    CultureID CHAR(6) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductPhoto (101 rows)
CREATE TABLE IF NOT EXISTS Production.ProductPhoto (
    ProductPhotoID NUMBER(38,0) DEFAULT Production.PRODUCTION_PRODUCTPHOTO_PRODUCTPHOTOID_SEQ.NEXTVAL NOT NULL,
    ThumbNailPhoto BINARY(16777216) NULL,
    ThumbnailPhotoFileName VARCHAR(50) NULL,
    LargePhoto BINARY(16777216) NULL,
    LargePhotoFileName VARCHAR(50) NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductProductPhoto (504 rows)
CREATE TABLE IF NOT EXISTS Production.ProductProductPhoto (
    ProductID NUMBER(38,0) NOT NULL,
    ProductPhotoID NUMBER(38,0) NOT NULL,
    Primary VARCHAR(16777216) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductReview (4 rows)
CREATE TABLE IF NOT EXISTS Production.ProductReview (
    ProductReviewID NUMBER(38,0) DEFAULT Production.PRODUCTION_PRODUCTREVIEW_PRODUCTREVIEWID_SEQ.NEXTVAL NOT NULL,
    ProductID NUMBER(38,0) NOT NULL,
    ReviewerName VARCHAR(16777216) NOT NULL,
    ReviewDate TIMESTAMP_NTZ NOT NULL,
    EmailAddress VARCHAR(50) NOT NULL,
    Rating NUMBER(38,0) NOT NULL,
    Comments VARCHAR(3850) NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ProductSubcategory (37 rows)
CREATE TABLE IF NOT EXISTS Production.ProductSubcategory (
    ProductSubcategoryID NUMBER(38,0) DEFAULT Production.PRODUCTION_PRODUCTSUBCATEGORY_PRODUCTSUBCATEGORYID_SEQ.NEXTVAL NOT NULL,
    ProductCategoryID NUMBER(38,0) NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.ScrapReason (16 rows)
CREATE TABLE IF NOT EXISTS Production.ScrapReason (
    ScrapReasonID NUMBER(38,0) DEFAULT Production.PRODUCTION_SCRAPREASON_SCRAPREASONID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.TransactionHistory (113,443 rows)
CREATE TABLE IF NOT EXISTS Production.TransactionHistory (
    TransactionID NUMBER(38,0) DEFAULT Production.PRODUCTION_TRANSACTIONHISTORY_TRANSACTIONID_SEQ.NEXTVAL NOT NULL,
    ProductID NUMBER(38,0) NOT NULL,
    ReferenceOrderID NUMBER(38,0) NOT NULL,
    ReferenceOrderLineID NUMBER(38,0) NOT NULL,
    TransactionDate TIMESTAMP_NTZ NOT NULL,
    TransactionType CHAR(1) NOT NULL,
    Quantity NUMBER(38,0) NOT NULL,
    ActualCost NUMBER(19,4) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.TransactionHistoryArchive (89,253 rows)
CREATE TABLE IF NOT EXISTS Production.TransactionHistoryArchive (
    TransactionID NUMBER(38,0) NOT NULL,
    ProductID NUMBER(38,0) NOT NULL,
    ReferenceOrderID NUMBER(38,0) NOT NULL,
    ReferenceOrderLineID NUMBER(38,0) NOT NULL,
    TransactionDate TIMESTAMP_NTZ NOT NULL,
    TransactionType CHAR(1) NOT NULL,
    Quantity NUMBER(38,0) NOT NULL,
    ActualCost NUMBER(19,4) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.UnitMeasure (38 rows)
CREATE TABLE IF NOT EXISTS Production.UnitMeasure (
    UnitMeasureCode CHAR(3) NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.WorkOrder (72,591 rows)
CREATE TABLE IF NOT EXISTS Production.WorkOrder (
    WorkOrderID NUMBER(38,0) DEFAULT Production.PRODUCTION_WORKORDER_WORKORDERID_SEQ.NEXTVAL NOT NULL,
    ProductID NUMBER(38,0) NOT NULL,
    OrderQty NUMBER(38,0) NOT NULL,
    StockedQty NUMBER(38,0) NOT NULL,
    ScrappedQty NUMBER(38,0) NOT NULL,
    StartDate TIMESTAMP_NTZ NOT NULL,
    EndDate TIMESTAMP_NTZ NULL,
    DueDate TIMESTAMP_NTZ NOT NULL,
    ScrapReasonID NUMBER(38,0) NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Production.WorkOrderRouting (67,131 rows)
CREATE TABLE IF NOT EXISTS Production.WorkOrderRouting (
    WorkOrderID NUMBER(38,0) NOT NULL,
    ProductID NUMBER(38,0) NOT NULL,
    OperationSequence NUMBER(38,0) NOT NULL,
    LocationID NUMBER(38,0) NOT NULL,
    ScheduledStartDate TIMESTAMP_NTZ NOT NULL,
    ScheduledEndDate TIMESTAMP_NTZ NOT NULL,
    ActualStartDate TIMESTAMP_NTZ NULL,
    ActualEndDate TIMESTAMP_NTZ NULL,
    ActualResourceHrs NUMBER(9,4) NULL,
    PlannedCost NUMBER(19,4) NOT NULL,
    ActualCost NUMBER(19,4) NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Purchasing.ProductVendor (460 rows)
CREATE TABLE IF NOT EXISTS Purchasing.ProductVendor (
    ProductID NUMBER(38,0) NOT NULL,
    BusinessEntityID NUMBER(38,0) NOT NULL,
    AverageLeadTime NUMBER(38,0) NOT NULL,
    StandardPrice NUMBER(19,4) NOT NULL,
    LastReceiptCost NUMBER(19,4) NULL,
    LastReceiptDate TIMESTAMP_NTZ NULL,
    MinOrderQty NUMBER(38,0) NOT NULL,
    MaxOrderQty NUMBER(38,0) NOT NULL,
    OnOrderQty NUMBER(38,0) NULL,
    UnitMeasureCode CHAR(3) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Purchasing.PurchaseOrderDetail (8,845 rows)
CREATE TABLE IF NOT EXISTS Purchasing.PurchaseOrderDetail (
    PurchaseOrderID NUMBER(38,0) NOT NULL,
    PurchaseOrderDetailID NUMBER(38,0) DEFAULT Purchasing.PURCHASING_PURCHASEORDERDETAIL_PURCHASEORDERDETAILID_SEQ.NEXTVAL NOT NULL,
    DueDate TIMESTAMP_NTZ NOT NULL,
    OrderQty NUMBER(38,0) NOT NULL,
    ProductID NUMBER(38,0) NOT NULL,
    UnitPrice NUMBER(19,4) NOT NULL,
    LineTotal NUMBER(19,4) NOT NULL,
    ReceivedQty NUMBER(8,2) NOT NULL,
    RejectedQty NUMBER(8,2) NOT NULL,
    StockedQty NUMBER(9,2) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Purchasing.PurchaseOrderHeader (4,012 rows)
CREATE TABLE IF NOT EXISTS Purchasing.PurchaseOrderHeader (
    PurchaseOrderID NUMBER(38,0) DEFAULT Purchasing.PURCHASING_PURCHASEORDERHEADER_PURCHASEORDERID_SEQ.NEXTVAL NOT NULL,
    RevisionNumber NUMBER(38,0) NOT NULL,
    Status NUMBER(38,0) NOT NULL,
    EmployeeID NUMBER(38,0) NOT NULL,
    VendorID NUMBER(38,0) NOT NULL,
    ShipMethodID NUMBER(38,0) NOT NULL,
    OrderDate TIMESTAMP_NTZ NOT NULL,
    ShipDate TIMESTAMP_NTZ NULL,
    SubTotal NUMBER(19,4) NOT NULL,
    TaxAmt NUMBER(19,4) NOT NULL,
    Freight NUMBER(19,4) NOT NULL,
    TotalDue NUMBER(19,4) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Purchasing.ShipMethod (5 rows)
CREATE TABLE IF NOT EXISTS Purchasing.ShipMethod (
    ShipMethodID NUMBER(38,0) DEFAULT Purchasing.PURCHASING_SHIPMETHOD_SHIPMETHODID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    ShipBase NUMBER(19,4) NOT NULL,
    ShipRate NUMBER(19,4) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Purchasing.Vendor (104 rows)
CREATE TABLE IF NOT EXISTS Purchasing.Vendor (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    AccountNumber VARCHAR(16777216) NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    CreditRating NUMBER(38,0) NOT NULL,
    PreferredVendorStatus VARCHAR(16777216) NOT NULL,
    ActiveFlag VARCHAR(16777216) NOT NULL,
    PurchasingWebServiceURL VARCHAR(1024) NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.CountryRegionCurrency (109 rows)
CREATE TABLE IF NOT EXISTS Sales.CountryRegionCurrency (
    CountryRegionCode VARCHAR(3) NOT NULL,
    CurrencyCode CHAR(3) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.CreditCard (19,118 rows)
CREATE TABLE IF NOT EXISTS Sales.CreditCard (
    CreditCardID NUMBER(38,0) DEFAULT Sales.SALES_CREDITCARD_CREDITCARDID_SEQ.NEXTVAL NOT NULL,
    CardType VARCHAR(50) NOT NULL,
    CardNumber VARCHAR(25) NOT NULL,
    ExpMonth NUMBER(38,0) NOT NULL,
    ExpYear NUMBER(38,0) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.Currency (105 rows)
CREATE TABLE IF NOT EXISTS Sales.Currency (
    CurrencyCode CHAR(3) NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.CurrencyRate (13,532 rows)
CREATE TABLE IF NOT EXISTS Sales.CurrencyRate (
    CurrencyRateID NUMBER(38,0) DEFAULT Sales.SALES_CURRENCYRATE_CURRENCYRATEID_SEQ.NEXTVAL NOT NULL,
    CurrencyRateDate TIMESTAMP_NTZ NOT NULL,
    FromCurrencyCode CHAR(3) NOT NULL,
    ToCurrencyCode CHAR(3) NOT NULL,
    AverageRate NUMBER(19,4) NOT NULL,
    EndOfDayRate NUMBER(19,4) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.Customer (19,820 rows)
CREATE TABLE IF NOT EXISTS Sales.Customer (
    CustomerID NUMBER(38,0) DEFAULT Sales.SALES_CUSTOMER_CUSTOMERID_SEQ.NEXTVAL NOT NULL,
    PersonID NUMBER(38,0) NULL,
    StoreID NUMBER(38,0) NULL,
    TerritoryID NUMBER(38,0) NULL,
    AccountNumber VARCHAR(10) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.PersonCreditCard (19,118 rows)
CREATE TABLE IF NOT EXISTS Sales.PersonCreditCard (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    CreditCardID NUMBER(38,0) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.SalesOrderDetail (121,317 rows)
CREATE TABLE IF NOT EXISTS Sales.SalesOrderDetail (
    SalesOrderID NUMBER(38,0) NOT NULL,
    SalesOrderDetailID NUMBER(38,0) DEFAULT Sales.SALES_SALESORDERDETAIL_SALESORDERDETAILID_SEQ.NEXTVAL NOT NULL,
    CarrierTrackingNumber VARCHAR(25) NULL,
    OrderQty NUMBER(38,0) NOT NULL,
    ProductID NUMBER(38,0) NOT NULL,
    SpecialOfferID NUMBER(38,0) NOT NULL,
    UnitPrice NUMBER(19,4) NOT NULL,
    UnitPriceDiscount NUMBER(19,4) NOT NULL,
    LineTotal NUMBER(38,6) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.SalesOrderHeader (31,465 rows)
CREATE TABLE IF NOT EXISTS Sales.SalesOrderHeader (
    SalesOrderID NUMBER(38,0) DEFAULT Sales.SALES_SALESORDERHEADER_SALESORDERID_SEQ.NEXTVAL NOT NULL,
    RevisionNumber NUMBER(38,0) NOT NULL,
    OrderDate TIMESTAMP_NTZ NOT NULL,
    DueDate TIMESTAMP_NTZ NOT NULL,
    ShipDate TIMESTAMP_NTZ NULL,
    Status NUMBER(38,0) NOT NULL,
    OnlineOrderFlag VARCHAR(16777216) NOT NULL,
    SalesOrderNumber VARCHAR(25) NOT NULL,
    PurchaseOrderNumber VARCHAR(16777216) NULL,
    AccountNumber VARCHAR(16777216) NULL,
    CustomerID NUMBER(38,0) NOT NULL,
    SalesPersonID NUMBER(38,0) NULL,
    TerritoryID NUMBER(38,0) NULL,
    BillToAddressID NUMBER(38,0) NOT NULL,
    ShipToAddressID NUMBER(38,0) NOT NULL,
    ShipMethodID NUMBER(38,0) NOT NULL,
    CreditCardID NUMBER(38,0) NULL,
    CreditCardApprovalCode VARCHAR(15) NULL,
    CurrencyRateID NUMBER(38,0) NULL,
    SubTotal NUMBER(19,4) NOT NULL,
    TaxAmt NUMBER(19,4) NOT NULL,
    Freight NUMBER(19,4) NOT NULL,
    TotalDue NUMBER(19,4) NOT NULL,
    Comment VARCHAR(128) NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.SalesOrderHeaderSalesReason (27,647 rows)
CREATE TABLE IF NOT EXISTS Sales.SalesOrderHeaderSalesReason (
    SalesOrderID NUMBER(38,0) NOT NULL,
    SalesReasonID NUMBER(38,0) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.SalesPerson (17 rows)
CREATE TABLE IF NOT EXISTS Sales.SalesPerson (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    TerritoryID NUMBER(38,0) NULL,
    SalesQuota NUMBER(19,4) NULL,
    Bonus NUMBER(19,4) NOT NULL,
    CommissionPct NUMBER(10,4) NOT NULL,
    SalesYTD NUMBER(19,4) NOT NULL,
    SalesLastYear NUMBER(19,4) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.SalesPersonQuotaHistory (163 rows)
CREATE TABLE IF NOT EXISTS Sales.SalesPersonQuotaHistory (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    QuotaDate TIMESTAMP_NTZ NOT NULL,
    SalesQuota NUMBER(19,4) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.SalesReason (10 rows)
CREATE TABLE IF NOT EXISTS Sales.SalesReason (
    SalesReasonID NUMBER(38,0) DEFAULT Sales.SALES_SALESREASON_SALESREASONID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    ReasonType VARCHAR(16777216) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.SalesTaxRate (29 rows)
CREATE TABLE IF NOT EXISTS Sales.SalesTaxRate (
    SalesTaxRateID NUMBER(38,0) DEFAULT Sales.SALES_SALESTAXRATE_SALESTAXRATEID_SEQ.NEXTVAL NOT NULL,
    StateProvinceID NUMBER(38,0) NOT NULL,
    TaxType NUMBER(38,0) NOT NULL,
    TaxRate NUMBER(10,4) NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.SalesTerritory (10 rows)
CREATE TABLE IF NOT EXISTS Sales.SalesTerritory (
    TerritoryID NUMBER(38,0) DEFAULT Sales.SALES_SALESTERRITORY_TERRITORYID_SEQ.NEXTVAL NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    CountryRegionCode VARCHAR(3) NOT NULL,
    "Group" VARCHAR(50) NOT NULL,
    SalesYTD NUMBER(19,4) NOT NULL,
    SalesLastYear NUMBER(19,4) NOT NULL,
    CostYTD NUMBER(19,4) NOT NULL,
    CostLastYear NUMBER(19,4) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.SalesTerritoryHistory (17 rows)
CREATE TABLE IF NOT EXISTS Sales.SalesTerritoryHistory (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    TerritoryID NUMBER(38,0) NOT NULL,
    StartDate TIMESTAMP_NTZ NOT NULL,
    EndDate TIMESTAMP_NTZ NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.ShoppingCartItem (3 rows)
CREATE TABLE IF NOT EXISTS Sales.ShoppingCartItem (
    ShoppingCartItemID NUMBER(38,0) DEFAULT Sales.SALES_SHOPPINGCARTITEM_SHOPPINGCARTITEMID_SEQ.NEXTVAL NOT NULL,
    ShoppingCartID VARCHAR(50) NOT NULL,
    Quantity NUMBER(38,0) NOT NULL,
    ProductID NUMBER(38,0) NOT NULL,
    DateCreated TIMESTAMP_NTZ NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.SpecialOffer (16 rows)
CREATE TABLE IF NOT EXISTS Sales.SpecialOffer (
    SpecialOfferID NUMBER(38,0) DEFAULT Sales.SALES_SPECIALOFFER_SPECIALOFFERID_SEQ.NEXTVAL NOT NULL,
    Description VARCHAR(255) NOT NULL,
    DiscountPct NUMBER(10,4) NOT NULL,
    Type VARCHAR(50) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    StartDate TIMESTAMP_NTZ NOT NULL,
    EndDate TIMESTAMP_NTZ NOT NULL,
    MinQty NUMBER(38,0) NOT NULL,
    MaxQty NUMBER(38,0) NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.SpecialOfferProduct (538 rows)
CREATE TABLE IF NOT EXISTS Sales.SpecialOfferProduct (
    SpecialOfferID NUMBER(38,0) NOT NULL,
    ProductID NUMBER(38,0) NOT NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);

-- Table: Sales.Store (701 rows)
CREATE TABLE IF NOT EXISTS Sales.Store (
    BusinessEntityID NUMBER(38,0) NOT NULL,
    Name VARCHAR(16777216) NOT NULL,
    SalesPersonID NUMBER(38,0) NULL,
    Demographics VARCHAR(16777216) NULL,
    rowguid VARCHAR(36) NOT NULL,
    ModifiedDate TIMESTAMP_NTZ NOT NULL
);
