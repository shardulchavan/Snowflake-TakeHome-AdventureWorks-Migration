-- =============================================
-- Foreign Key Constraints (Informational)
-- Note: Snowflake doesn't enforce FKs, but they aid query optimization
-- =============================================

ALTER TABLE Humanresources.Employee
    ADD CONSTRAINT FK_Employee_Person_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Person.Person(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Humanresources.EmployeeDepartmentHistory
    ADD CONSTRAINT FK_EmployeeDepartmentHistory_Department_DepartmentID
    FOREIGN KEY (DepartmentID)
    REFERENCES Humanresources.Department(DepartmentID)
    NOT ENFORCED;

ALTER TABLE Humanresources.EmployeeDepartmentHistory
    ADD CONSTRAINT FK_EmployeeDepartmentHistory_Employee_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Humanresources.Employee(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Humanresources.EmployeeDepartmentHistory
    ADD CONSTRAINT FK_EmployeeDepartmentHistory_Shift_ShiftID
    FOREIGN KEY (ShiftID)
    REFERENCES Humanresources.Shift(ShiftID)
    NOT ENFORCED;

ALTER TABLE Humanresources.EmployeePayHistory
    ADD CONSTRAINT FK_EmployeePayHistory_Employee_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Humanresources.Employee(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Humanresources.JobCandidate
    ADD CONSTRAINT FK_JobCandidate_Employee_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Humanresources.Employee(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Person.Address
    ADD CONSTRAINT FK_Address_StateProvince_StateProvinceID
    FOREIGN KEY (StateProvinceID)
    REFERENCES Person.StateProvince(StateProvinceID)
    NOT ENFORCED;

ALTER TABLE Person.BusinessEntityAddress
    ADD CONSTRAINT FK_BusinessEntityAddress_Address_AddressID
    FOREIGN KEY (AddressID)
    REFERENCES Person.Address(AddressID)
    NOT ENFORCED;

ALTER TABLE Person.BusinessEntityAddress
    ADD CONSTRAINT FK_BusinessEntityAddress_AddressType_AddressTypeID
    FOREIGN KEY (AddressTypeID)
    REFERENCES Person.AddressType(AddressTypeID)
    NOT ENFORCED;

ALTER TABLE Person.BusinessEntityAddress
    ADD CONSTRAINT FK_BusinessEntityAddress_BusinessEntity_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Person.BusinessEntity(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Person.BusinessEntityContact
    ADD CONSTRAINT FK_BusinessEntityContact_BusinessEntity_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Person.BusinessEntity(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Person.BusinessEntityContact
    ADD CONSTRAINT FK_BusinessEntityContact_ContactType_ContactTypeID
    FOREIGN KEY (ContactTypeID)
    REFERENCES Person.ContactType(ContactTypeID)
    NOT ENFORCED;

ALTER TABLE Person.BusinessEntityContact
    ADD CONSTRAINT FK_BusinessEntityContact_Person_PersonID
    FOREIGN KEY (PersonID)
    REFERENCES Person.Person(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Person.EmailAddress
    ADD CONSTRAINT FK_EmailAddress_Person_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Person.Person(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Person.Password
    ADD CONSTRAINT FK_Password_Person_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Person.Person(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Person.Person
    ADD CONSTRAINT FK_Person_BusinessEntity_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Person.BusinessEntity(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Person.PersonPhone
    ADD CONSTRAINT FK_PersonPhone_Person_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Person.Person(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Person.PersonPhone
    ADD CONSTRAINT FK_PersonPhone_PhoneNumberType_PhoneNumberTypeID
    FOREIGN KEY (PhoneNumberTypeID)
    REFERENCES Person.PhoneNumberType(PhoneNumberTypeID)
    NOT ENFORCED;

ALTER TABLE Person.StateProvince
    ADD CONSTRAINT FK_StateProvince_CountryRegion_CountryRegionCode
    FOREIGN KEY (CountryRegionCode)
    REFERENCES Person.CountryRegion(CountryRegionCode)
    NOT ENFORCED;

ALTER TABLE Person.StateProvince
    ADD CONSTRAINT FK_StateProvince_SalesTerritory_TerritoryID
    FOREIGN KEY (TerritoryID)
    REFERENCES Sales.SalesTerritory(TerritoryID)
    NOT ENFORCED;

ALTER TABLE Production.BillOfMaterials
    ADD CONSTRAINT FK_BillOfMaterials_Product_ComponentID
    FOREIGN KEY (ComponentID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Production.BillOfMaterials
    ADD CONSTRAINT FK_BillOfMaterials_Product_ProductAssemblyID
    FOREIGN KEY (ProductAssemblyID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Production.BillOfMaterials
    ADD CONSTRAINT FK_BillOfMaterials_UnitMeasure_UnitMeasureCode
    FOREIGN KEY (UnitMeasureCode)
    REFERENCES Production.UnitMeasure(UnitMeasureCode)
    NOT ENFORCED;

ALTER TABLE Production.Document
    ADD CONSTRAINT FK_Document_Employee_Owner
    FOREIGN KEY (Owner)
    REFERENCES Humanresources.Employee(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Production.Product
    ADD CONSTRAINT FK_Product_ProductModel_ProductModelID
    FOREIGN KEY (ProductModelID)
    REFERENCES Production.ProductModel(ProductModelID)
    NOT ENFORCED;

ALTER TABLE Production.Product
    ADD CONSTRAINT FK_Product_ProductSubcategory_ProductSubcategoryID
    FOREIGN KEY (ProductSubcategoryID)
    REFERENCES Production.ProductSubcategory(ProductSubcategoryID)
    NOT ENFORCED;

ALTER TABLE Production.Product
    ADD CONSTRAINT FK_Product_UnitMeasure_SizeUnitMeasureCode
    FOREIGN KEY (SizeUnitMeasureCode)
    REFERENCES Production.UnitMeasure(UnitMeasureCode)
    NOT ENFORCED;

ALTER TABLE Production.Product
    ADD CONSTRAINT FK_Product_UnitMeasure_WeightUnitMeasureCode
    FOREIGN KEY (WeightUnitMeasureCode)
    REFERENCES Production.UnitMeasure(UnitMeasureCode)
    NOT ENFORCED;

ALTER TABLE Production.ProductCostHistory
    ADD CONSTRAINT FK_ProductCostHistory_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Production.ProductDocument
    ADD CONSTRAINT FK_ProductDocument_Document_DocumentNode
    FOREIGN KEY (DocumentNode)
    REFERENCES Production.Document(DocumentNode)
    NOT ENFORCED;

ALTER TABLE Production.ProductDocument
    ADD CONSTRAINT FK_ProductDocument_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Production.ProductInventory
    ADD CONSTRAINT FK_ProductInventory_Location_LocationID
    FOREIGN KEY (LocationID)
    REFERENCES Production.Location(LocationID)
    NOT ENFORCED;

ALTER TABLE Production.ProductInventory
    ADD CONSTRAINT FK_ProductInventory_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Production.ProductListPriceHistory
    ADD CONSTRAINT FK_ProductListPriceHistory_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Production.ProductModelIllustration
    ADD CONSTRAINT FK_ProductModelIllustration_Illustration_IllustrationID
    FOREIGN KEY (IllustrationID)
    REFERENCES Production.Illustration(IllustrationID)
    NOT ENFORCED;

ALTER TABLE Production.ProductModelIllustration
    ADD CONSTRAINT FK_ProductModelIllustration_ProductModel_ProductModelID
    FOREIGN KEY (ProductModelID)
    REFERENCES Production.ProductModel(ProductModelID)
    NOT ENFORCED;

ALTER TABLE Production.ProductModelProductDescriptionCulture
    ADD CONSTRAINT FK_ProductModelProductDescriptionCulture_Culture_CultureID
    FOREIGN KEY (CultureID)
    REFERENCES Production.Culture(CultureID)
    NOT ENFORCED;

ALTER TABLE Production.ProductModelProductDescriptionCulture
    ADD CONSTRAINT FK_ProductModelProductDescriptionCulture_ProductDescription_ProductDescriptionID
    FOREIGN KEY (ProductDescriptionID)
    REFERENCES Production.ProductDescription(ProductDescriptionID)
    NOT ENFORCED;

ALTER TABLE Production.ProductModelProductDescriptionCulture
    ADD CONSTRAINT FK_ProductModelProductDescriptionCulture_ProductModel_ProductModelID
    FOREIGN KEY (ProductModelID)
    REFERENCES Production.ProductModel(ProductModelID)
    NOT ENFORCED;

ALTER TABLE Production.ProductProductPhoto
    ADD CONSTRAINT FK_ProductProductPhoto_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Production.ProductProductPhoto
    ADD CONSTRAINT FK_ProductProductPhoto_ProductPhoto_ProductPhotoID
    FOREIGN KEY (ProductPhotoID)
    REFERENCES Production.ProductPhoto(ProductPhotoID)
    NOT ENFORCED;

ALTER TABLE Production.ProductReview
    ADD CONSTRAINT FK_ProductReview_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Production.ProductSubcategory
    ADD CONSTRAINT FK_ProductSubcategory_ProductCategory_ProductCategoryID
    FOREIGN KEY (ProductCategoryID)
    REFERENCES Production.ProductCategory(ProductCategoryID)
    NOT ENFORCED;

ALTER TABLE Production.TransactionHistory
    ADD CONSTRAINT FK_TransactionHistory_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Production.WorkOrder
    ADD CONSTRAINT FK_WorkOrder_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Production.WorkOrder
    ADD CONSTRAINT FK_WorkOrder_ScrapReason_ScrapReasonID
    FOREIGN KEY (ScrapReasonID)
    REFERENCES Production.ScrapReason(ScrapReasonID)
    NOT ENFORCED;

ALTER TABLE Production.WorkOrderRouting
    ADD CONSTRAINT FK_WorkOrderRouting_Location_LocationID
    FOREIGN KEY (LocationID)
    REFERENCES Production.Location(LocationID)
    NOT ENFORCED;

ALTER TABLE Production.WorkOrderRouting
    ADD CONSTRAINT FK_WorkOrderRouting_WorkOrder_WorkOrderID
    FOREIGN KEY (WorkOrderID)
    REFERENCES Production.WorkOrder(WorkOrderID)
    NOT ENFORCED;

ALTER TABLE Purchasing.ProductVendor
    ADD CONSTRAINT FK_ProductVendor_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Purchasing.ProductVendor
    ADD CONSTRAINT FK_ProductVendor_UnitMeasure_UnitMeasureCode
    FOREIGN KEY (UnitMeasureCode)
    REFERENCES Production.UnitMeasure(UnitMeasureCode)
    NOT ENFORCED;

ALTER TABLE Purchasing.ProductVendor
    ADD CONSTRAINT FK_ProductVendor_Vendor_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Purchasing.Vendor(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Purchasing.PurchaseOrderDetail
    ADD CONSTRAINT FK_PurchaseOrderDetail_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Purchasing.PurchaseOrderDetail
    ADD CONSTRAINT FK_PurchaseOrderDetail_PurchaseOrderHeader_PurchaseOrderID
    FOREIGN KEY (PurchaseOrderID)
    REFERENCES Purchasing.PurchaseOrderHeader(PurchaseOrderID)
    NOT ENFORCED;

ALTER TABLE Purchasing.PurchaseOrderHeader
    ADD CONSTRAINT FK_PurchaseOrderHeader_Employee_EmployeeID
    FOREIGN KEY (EmployeeID)
    REFERENCES Humanresources.Employee(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Purchasing.PurchaseOrderHeader
    ADD CONSTRAINT FK_PurchaseOrderHeader_ShipMethod_ShipMethodID
    FOREIGN KEY (ShipMethodID)
    REFERENCES Purchasing.ShipMethod(ShipMethodID)
    NOT ENFORCED;

ALTER TABLE Purchasing.PurchaseOrderHeader
    ADD CONSTRAINT FK_PurchaseOrderHeader_Vendor_VendorID
    FOREIGN KEY (VendorID)
    REFERENCES Purchasing.Vendor(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Purchasing.Vendor
    ADD CONSTRAINT FK_Vendor_BusinessEntity_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Person.BusinessEntity(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Sales.CountryRegionCurrency
    ADD CONSTRAINT FK_CountryRegionCurrency_CountryRegion_CountryRegionCode
    FOREIGN KEY (CountryRegionCode)
    REFERENCES Person.CountryRegion(CountryRegionCode)
    NOT ENFORCED;

ALTER TABLE Sales.CountryRegionCurrency
    ADD CONSTRAINT FK_CountryRegionCurrency_Currency_CurrencyCode
    FOREIGN KEY (CurrencyCode)
    REFERENCES Sales.Currency(CurrencyCode)
    NOT ENFORCED;

ALTER TABLE Sales.CurrencyRate
    ADD CONSTRAINT FK_CurrencyRate_Currency_FromCurrencyCode
    FOREIGN KEY (FromCurrencyCode)
    REFERENCES Sales.Currency(CurrencyCode)
    NOT ENFORCED;

ALTER TABLE Sales.CurrencyRate
    ADD CONSTRAINT FK_CurrencyRate_Currency_ToCurrencyCode
    FOREIGN KEY (ToCurrencyCode)
    REFERENCES Sales.Currency(CurrencyCode)
    NOT ENFORCED;

ALTER TABLE Sales.Customer
    ADD CONSTRAINT FK_Customer_Person_PersonID
    FOREIGN KEY (PersonID)
    REFERENCES Person.Person(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Sales.Customer
    ADD CONSTRAINT FK_Customer_SalesTerritory_TerritoryID
    FOREIGN KEY (TerritoryID)
    REFERENCES Sales.SalesTerritory(TerritoryID)
    NOT ENFORCED;

ALTER TABLE Sales.Customer
    ADD CONSTRAINT FK_Customer_Store_StoreID
    FOREIGN KEY (StoreID)
    REFERENCES Sales.Store(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Sales.PersonCreditCard
    ADD CONSTRAINT FK_PersonCreditCard_CreditCard_CreditCardID
    FOREIGN KEY (CreditCardID)
    REFERENCES Sales.CreditCard(CreditCardID)
    NOT ENFORCED;

ALTER TABLE Sales.PersonCreditCard
    ADD CONSTRAINT FK_PersonCreditCard_Person_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Person.Person(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderDetail
    ADD CONSTRAINT FK_SalesOrderDetail_SalesOrderHeader_SalesOrderID
    FOREIGN KEY (SalesOrderID)
    REFERENCES Sales.SalesOrderHeader(SalesOrderID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderDetail
    ADD CONSTRAINT FK_SalesOrderDetail_SpecialOfferProduct_SpecialOfferIDProductID
    FOREIGN KEY (SpecialOfferID, ProductID)
    REFERENCES Sales.SpecialOfferProduct(SpecialOfferID, ProductID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeader
    ADD CONSTRAINT FK_SalesOrderHeader_Address_BillToAddressID
    FOREIGN KEY (BillToAddressID)
    REFERENCES Person.Address(AddressID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeader
    ADD CONSTRAINT FK_SalesOrderHeader_Address_ShipToAddressID
    FOREIGN KEY (ShipToAddressID)
    REFERENCES Person.Address(AddressID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeader
    ADD CONSTRAINT FK_SalesOrderHeader_CreditCard_CreditCardID
    FOREIGN KEY (CreditCardID)
    REFERENCES Sales.CreditCard(CreditCardID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeader
    ADD CONSTRAINT FK_SalesOrderHeader_CurrencyRate_CurrencyRateID
    FOREIGN KEY (CurrencyRateID)
    REFERENCES Sales.CurrencyRate(CurrencyRateID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeader
    ADD CONSTRAINT FK_SalesOrderHeader_Customer_CustomerID
    FOREIGN KEY (CustomerID)
    REFERENCES Sales.Customer(CustomerID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeader
    ADD CONSTRAINT FK_SalesOrderHeader_SalesPerson_SalesPersonID
    FOREIGN KEY (SalesPersonID)
    REFERENCES Sales.SalesPerson(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeader
    ADD CONSTRAINT FK_SalesOrderHeader_SalesTerritory_TerritoryID
    FOREIGN KEY (TerritoryID)
    REFERENCES Sales.SalesTerritory(TerritoryID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeader
    ADD CONSTRAINT FK_SalesOrderHeader_ShipMethod_ShipMethodID
    FOREIGN KEY (ShipMethodID)
    REFERENCES Purchasing.ShipMethod(ShipMethodID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeaderSalesReason
    ADD CONSTRAINT FK_SalesOrderHeaderSalesReason_SalesOrderHeader_SalesOrderID
    FOREIGN KEY (SalesOrderID)
    REFERENCES Sales.SalesOrderHeader(SalesOrderID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesOrderHeaderSalesReason
    ADD CONSTRAINT FK_SalesOrderHeaderSalesReason_SalesReason_SalesReasonID
    FOREIGN KEY (SalesReasonID)
    REFERENCES Sales.SalesReason(SalesReasonID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesPerson
    ADD CONSTRAINT FK_SalesPerson_Employee_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Humanresources.Employee(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesPerson
    ADD CONSTRAINT FK_SalesPerson_SalesTerritory_TerritoryID
    FOREIGN KEY (TerritoryID)
    REFERENCES Sales.SalesTerritory(TerritoryID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesPersonQuotaHistory
    ADD CONSTRAINT FK_SalesPersonQuotaHistory_SalesPerson_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Sales.SalesPerson(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesTaxRate
    ADD CONSTRAINT FK_SalesTaxRate_StateProvince_StateProvinceID
    FOREIGN KEY (StateProvinceID)
    REFERENCES Person.StateProvince(StateProvinceID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesTerritory
    ADD CONSTRAINT FK_SalesTerritory_CountryRegion_CountryRegionCode
    FOREIGN KEY (CountryRegionCode)
    REFERENCES Person.CountryRegion(CountryRegionCode)
    NOT ENFORCED;

ALTER TABLE Sales.SalesTerritoryHistory
    ADD CONSTRAINT FK_SalesTerritoryHistory_SalesPerson_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Sales.SalesPerson(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Sales.SalesTerritoryHistory
    ADD CONSTRAINT FK_SalesTerritoryHistory_SalesTerritory_TerritoryID
    FOREIGN KEY (TerritoryID)
    REFERENCES Sales.SalesTerritory(TerritoryID)
    NOT ENFORCED;

ALTER TABLE Sales.ShoppingCartItem
    ADD CONSTRAINT FK_ShoppingCartItem_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Sales.SpecialOfferProduct
    ADD CONSTRAINT FK_SpecialOfferProduct_Product_ProductID
    FOREIGN KEY (ProductID)
    REFERENCES Production.Product(ProductID)
    NOT ENFORCED;

ALTER TABLE Sales.SpecialOfferProduct
    ADD CONSTRAINT FK_SpecialOfferProduct_SpecialOffer_SpecialOfferID
    FOREIGN KEY (SpecialOfferID)
    REFERENCES Sales.SpecialOffer(SpecialOfferID)
    NOT ENFORCED;

ALTER TABLE Sales.Store
    ADD CONSTRAINT FK_Store_BusinessEntity_BusinessEntityID
    FOREIGN KEY (BusinessEntityID)
    REFERENCES Person.BusinessEntity(BusinessEntityID)
    NOT ENFORCED;

ALTER TABLE Sales.Store
    ADD CONSTRAINT FK_Store_SalesPerson_SalesPersonID
    FOREIGN KEY (SalesPersonID)
    REFERENCES Sales.SalesPerson(BusinessEntityID)
    NOT ENFORCED;
