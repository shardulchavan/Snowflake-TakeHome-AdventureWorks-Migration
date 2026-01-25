-- =============================================
-- Primary Key Constraints (Informational)
-- Note: Snowflake doesn't enforce PKs, but they aid query optimization
-- =============================================

ALTER TABLE DBO.AWBuildVersion
    ADD CONSTRAINT PK_AWBuildVersion_SystemInformationID PRIMARY KEY (SystemInformationID) NOT ENFORCED;

ALTER TABLE DBO.DatabaseLog
    ADD CONSTRAINT PK_DatabaseLog_DatabaseLogID PRIMARY KEY (DatabaseLogID) NOT ENFORCED;

ALTER TABLE DBO.ErrorLog
    ADD CONSTRAINT PK_ErrorLog_ErrorLogID PRIMARY KEY (ErrorLogID) NOT ENFORCED;

ALTER TABLE Humanresources.Department
    ADD CONSTRAINT PK_Department_DepartmentID PRIMARY KEY (DepartmentID) NOT ENFORCED;

ALTER TABLE Humanresources.Employee
    ADD CONSTRAINT PK_Employee_BusinessEntityID PRIMARY KEY (BusinessEntityID) NOT ENFORCED;

ALTER TABLE Humanresources.EmployeeDepartmentHistory
    ADD CONSTRAINT PK_EmployeeDepartmentHistory_BusinessEntityID_StartDate_DepartmentID PRIMARY KEY (BusinessEntityID, StartDate, DepartmentID, ShiftID) NOT ENFORCED;

ALTER TABLE Humanresources.EmployeePayHistory
    ADD CONSTRAINT PK_EmployeePayHistory_BusinessEntityID_RateChangeDate PRIMARY KEY (BusinessEntityID, RateChangeDate) NOT ENFORCED;

ALTER TABLE Humanresources.JobCandidate
    ADD CONSTRAINT PK_JobCandidate_JobCandidateID PRIMARY KEY (JobCandidateID) NOT ENFORCED;

ALTER TABLE Humanresources.Shift
    ADD CONSTRAINT PK_Shift_ShiftID PRIMARY KEY (ShiftID) NOT ENFORCED;

ALTER TABLE Person.Address
    ADD CONSTRAINT PK_Address_AddressID PRIMARY KEY (AddressID) NOT ENFORCED;

ALTER TABLE Person.AddressType
    ADD CONSTRAINT PK_AddressType_AddressTypeID PRIMARY KEY (AddressTypeID) NOT ENFORCED;

ALTER TABLE Person.BusinessEntity
    ADD CONSTRAINT PK_BusinessEntity_BusinessEntityID PRIMARY KEY (BusinessEntityID) NOT ENFORCED;

ALTER TABLE Person.BusinessEntityAddress
    ADD CONSTRAINT PK_BusinessEntityAddress_BusinessEntityID_AddressID_AddressTypeID PRIMARY KEY (BusinessEntityID, AddressID, AddressTypeID) NOT ENFORCED;

ALTER TABLE Person.BusinessEntityContact
    ADD CONSTRAINT PK_BusinessEntityContact_BusinessEntityID_PersonID_ContactTypeID PRIMARY KEY (BusinessEntityID, PersonID, ContactTypeID) NOT ENFORCED;

ALTER TABLE Person.ContactType
    ADD CONSTRAINT PK_ContactType_ContactTypeID PRIMARY KEY (ContactTypeID) NOT ENFORCED;

ALTER TABLE Person.CountryRegion
    ADD CONSTRAINT PK_CountryRegion_CountryRegionCode PRIMARY KEY (CountryRegionCode) NOT ENFORCED;

ALTER TABLE Person.EmailAddress
    ADD CONSTRAINT PK_EmailAddress_BusinessEntityID_EmailAddressID PRIMARY KEY (BusinessEntityID, EmailAddressID) NOT ENFORCED;

ALTER TABLE Person.Password
    ADD CONSTRAINT PK_Password_BusinessEntityID PRIMARY KEY (BusinessEntityID) NOT ENFORCED;

ALTER TABLE Person.Person
    ADD CONSTRAINT PK_Person_BusinessEntityID PRIMARY KEY (BusinessEntityID) NOT ENFORCED;

ALTER TABLE Person.PersonPhone
    ADD CONSTRAINT PK_PersonPhone_BusinessEntityID_PhoneNumber_PhoneNumberTypeID PRIMARY KEY (BusinessEntityID, PhoneNumber, PhoneNumberTypeID) NOT ENFORCED;

ALTER TABLE Person.PhoneNumberType
    ADD CONSTRAINT PK_PhoneNumberType_PhoneNumberTypeID PRIMARY KEY (PhoneNumberTypeID) NOT ENFORCED;

ALTER TABLE Person.StateProvince
    ADD CONSTRAINT PK_StateProvince_StateProvinceID PRIMARY KEY (StateProvinceID) NOT ENFORCED;

ALTER TABLE Production.BillOfMaterials
    ADD CONSTRAINT PK_BillOfMaterials_BillOfMaterialsID PRIMARY KEY (BillOfMaterialsID) NOT ENFORCED;

ALTER TABLE Production.Culture
    ADD CONSTRAINT PK_Culture_CultureID PRIMARY KEY (CultureID) NOT ENFORCED;

ALTER TABLE Production.Document
    ADD CONSTRAINT PK_Document_DocumentNode PRIMARY KEY (DocumentNode) NOT ENFORCED;

ALTER TABLE Production.Illustration
    ADD CONSTRAINT PK_Illustration_IllustrationID PRIMARY KEY (IllustrationID) NOT ENFORCED;

ALTER TABLE Production.Location
    ADD CONSTRAINT PK_Location_LocationID PRIMARY KEY (LocationID) NOT ENFORCED;

ALTER TABLE Production.Product
    ADD CONSTRAINT PK_Product_ProductID PRIMARY KEY (ProductID) NOT ENFORCED;

ALTER TABLE Production.ProductCategory
    ADD CONSTRAINT PK_ProductCategory_ProductCategoryID PRIMARY KEY (ProductCategoryID) NOT ENFORCED;

ALTER TABLE Production.ProductCostHistory
    ADD CONSTRAINT PK_ProductCostHistory_ProductID_StartDate PRIMARY KEY (ProductID, StartDate) NOT ENFORCED;

ALTER TABLE Production.ProductDescription
    ADD CONSTRAINT PK_ProductDescription_ProductDescriptionID PRIMARY KEY (ProductDescriptionID) NOT ENFORCED;

ALTER TABLE Production.ProductDocument
    ADD CONSTRAINT PK_ProductDocument_ProductID_DocumentNode PRIMARY KEY (ProductID, DocumentNode) NOT ENFORCED;

ALTER TABLE Production.ProductInventory
    ADD CONSTRAINT PK_ProductInventory_ProductID_LocationID PRIMARY KEY (ProductID, LocationID) NOT ENFORCED;

ALTER TABLE Production.ProductListPriceHistory
    ADD CONSTRAINT PK_ProductListPriceHistory_ProductID_StartDate PRIMARY KEY (ProductID, StartDate) NOT ENFORCED;

ALTER TABLE Production.ProductModel
    ADD CONSTRAINT PK_ProductModel_ProductModelID PRIMARY KEY (ProductModelID) NOT ENFORCED;

ALTER TABLE Production.ProductModelIllustration
    ADD CONSTRAINT PK_ProductModelIllustration_ProductModelID_IllustrationID PRIMARY KEY (ProductModelID, IllustrationID) NOT ENFORCED;

ALTER TABLE Production.ProductModelProductDescriptionCulture
    ADD CONSTRAINT PK_ProductModelProductDescriptionCulture_ProductModelID_ProductDescriptionID_CultureID PRIMARY KEY (ProductModelID, ProductDescriptionID, CultureID) NOT ENFORCED;

ALTER TABLE Production.ProductPhoto
    ADD CONSTRAINT PK_ProductPhoto_ProductPhotoID PRIMARY KEY (ProductPhotoID) NOT ENFORCED;

ALTER TABLE Production.ProductProductPhoto
    ADD CONSTRAINT PK_ProductProductPhoto_ProductID_ProductPhotoID PRIMARY KEY (ProductID, ProductPhotoID) NOT ENFORCED;

ALTER TABLE Production.ProductReview
    ADD CONSTRAINT PK_ProductReview_ProductReviewID PRIMARY KEY (ProductReviewID) NOT ENFORCED;

ALTER TABLE Production.ProductSubcategory
    ADD CONSTRAINT PK_ProductSubcategory_ProductSubcategoryID PRIMARY KEY (ProductSubcategoryID) NOT ENFORCED;

ALTER TABLE Production.ScrapReason
    ADD CONSTRAINT PK_ScrapReason_ScrapReasonID PRIMARY KEY (ScrapReasonID) NOT ENFORCED;

ALTER TABLE Production.TransactionHistory
    ADD CONSTRAINT PK_TransactionHistory_TransactionID PRIMARY KEY (TransactionID) NOT ENFORCED;

ALTER TABLE Production.TransactionHistoryArchive
    ADD CONSTRAINT PK_TransactionHistoryArchive_TransactionID PRIMARY KEY (TransactionID) NOT ENFORCED;

ALTER TABLE Production.UnitMeasure
    ADD CONSTRAINT PK_UnitMeasure_UnitMeasureCode PRIMARY KEY (UnitMeasureCode) NOT ENFORCED;

ALTER TABLE Production.WorkOrder
    ADD CONSTRAINT PK_WorkOrder_WorkOrderID PRIMARY KEY (WorkOrderID) NOT ENFORCED;

ALTER TABLE Production.WorkOrderRouting
    ADD CONSTRAINT PK_WorkOrderRouting_WorkOrderID_ProductID_OperationSequence PRIMARY KEY (WorkOrderID, ProductID, OperationSequence) NOT ENFORCED;

ALTER TABLE Purchasing.ProductVendor
    ADD CONSTRAINT PK_ProductVendor_ProductID_BusinessEntityID PRIMARY KEY (ProductID, BusinessEntityID) NOT ENFORCED;

ALTER TABLE Purchasing.PurchaseOrderDetail
    ADD CONSTRAINT PK_PurchaseOrderDetail_PurchaseOrderID_PurchaseOrderDetailID PRIMARY KEY (PurchaseOrderID, PurchaseOrderDetailID) NOT ENFORCED;

ALTER TABLE Purchasing.PurchaseOrderHeader
    ADD CONSTRAINT PK_PurchaseOrderHeader_PurchaseOrderID PRIMARY KEY (PurchaseOrderID) NOT ENFORCED;

ALTER TABLE Purchasing.ShipMethod
    ADD CONSTRAINT PK_ShipMethod_ShipMethodID PRIMARY KEY (ShipMethodID) NOT ENFORCED;

ALTER TABLE Purchasing.Vendor
    ADD CONSTRAINT PK_Vendor_BusinessEntityID PRIMARY KEY (BusinessEntityID) NOT ENFORCED;

ALTER TABLE Sales.CountryRegionCurrency
    ADD CONSTRAINT PK_CountryRegionCurrency_CountryRegionCode_CurrencyCode PRIMARY KEY (CountryRegionCode, CurrencyCode) NOT ENFORCED;

ALTER TABLE Sales.CreditCard
    ADD CONSTRAINT PK_CreditCard_CreditCardID PRIMARY KEY (CreditCardID) NOT ENFORCED;

ALTER TABLE Sales.Currency
    ADD CONSTRAINT PK_Currency_CurrencyCode PRIMARY KEY (CurrencyCode) NOT ENFORCED;

ALTER TABLE Sales.CurrencyRate
    ADD CONSTRAINT PK_CurrencyRate_CurrencyRateID PRIMARY KEY (CurrencyRateID) NOT ENFORCED;

ALTER TABLE Sales.Customer
    ADD CONSTRAINT PK_Customer_CustomerID PRIMARY KEY (CustomerID) NOT ENFORCED;

ALTER TABLE Sales.PersonCreditCard
    ADD CONSTRAINT PK_PersonCreditCard_BusinessEntityID_CreditCardID PRIMARY KEY (BusinessEntityID, CreditCardID) NOT ENFORCED;

ALTER TABLE Sales.SalesOrderDetail
    ADD CONSTRAINT PK_SalesOrderDetail_SalesOrderID_SalesOrderDetailID PRIMARY KEY (SalesOrderID, SalesOrderDetailID) NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeader
    ADD CONSTRAINT PK_SalesOrderHeader_SalesOrderID PRIMARY KEY (SalesOrderID) NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeaderSalesReason
    ADD CONSTRAINT PK_SalesOrderHeaderSalesReason_SalesOrderID_SalesReasonID PRIMARY KEY (SalesOrderID, SalesReasonID) NOT ENFORCED;

ALTER TABLE Sales.SalesPerson
    ADD CONSTRAINT PK_SalesPerson_BusinessEntityID PRIMARY KEY (BusinessEntityID) NOT ENFORCED;

ALTER TABLE Sales.SalesPersonQuotaHistory
    ADD CONSTRAINT PK_SalesPersonQuotaHistory_BusinessEntityID_QuotaDate PRIMARY KEY (BusinessEntityID, QuotaDate) NOT ENFORCED;

ALTER TABLE Sales.SalesReason
    ADD CONSTRAINT PK_SalesReason_SalesReasonID PRIMARY KEY (SalesReasonID) NOT ENFORCED;

ALTER TABLE Sales.SalesTaxRate
    ADD CONSTRAINT PK_SalesTaxRate_SalesTaxRateID PRIMARY KEY (SalesTaxRateID) NOT ENFORCED;

ALTER TABLE Sales.SalesTerritory
    ADD CONSTRAINT PK_SalesTerritory_TerritoryID PRIMARY KEY (TerritoryID) NOT ENFORCED;

ALTER TABLE Sales.SalesTerritoryHistory
    ADD CONSTRAINT PK_SalesTerritoryHistory_BusinessEntityID_StartDate_TerritoryID PRIMARY KEY (BusinessEntityID, StartDate, TerritoryID) NOT ENFORCED;

ALTER TABLE Sales.ShoppingCartItem
    ADD CONSTRAINT PK_ShoppingCartItem_ShoppingCartItemID PRIMARY KEY (ShoppingCartItemID) NOT ENFORCED;

ALTER TABLE Sales.SpecialOffer
    ADD CONSTRAINT PK_SpecialOffer_SpecialOfferID PRIMARY KEY (SpecialOfferID) NOT ENFORCED;

ALTER TABLE Sales.SpecialOfferProduct
    ADD CONSTRAINT PK_SpecialOfferProduct_SpecialOfferID_ProductID PRIMARY KEY (SpecialOfferID, ProductID) NOT ENFORCED;

ALTER TABLE Sales.Store
    ADD CONSTRAINT PK_Store_BusinessEntityID PRIMARY KEY (BusinessEntityID) NOT ENFORCED;
