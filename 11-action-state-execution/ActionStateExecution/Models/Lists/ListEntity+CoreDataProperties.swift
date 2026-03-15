//
//  ListEntity+CoreDataProperties.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//
//

import Foundation
import CoreData


extension ListEntity {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<ListEntity> {
        return NSFetchRequest<ListEntity>(entityName: "ListEntity")
    }

    @NSManaged public var id: UUID?
    @NSManaged public var name: String?
    @NSManaged public var listItems: NSSet?
    @NSManaged public var fields: NSSet?

}

// MARK: Generated accessors for listItems
extension ListEntity {

    @objc(addListItemsObject:)
    @NSManaged public func addToListItems(_ value: ListItemEntity)

    @objc(removeListItemsObject:)
    @NSManaged public func removeFromListItems(_ value: ListItemEntity)

    @objc(addListItems:)
    @NSManaged public func addToListItems(_ values: NSSet)

    @objc(removeListItems:)
    @NSManaged public func removeFromListItems(_ values: NSSet)

}

// MARK: Generated accessors for fields
extension ListEntity {

    @objc(addFieldsObject:)
    @NSManaged public func addToFields(_ value: FieldEntity)

    @objc(removeFieldsObject:)
    @NSManaged public func removeFromFields(_ value: FieldEntity)

    @objc(addFields:)
    @NSManaged public func addToFields(_ values: NSSet)

    @objc(removeFields:)
    @NSManaged public func removeFromFields(_ values: NSSet)

}

extension ListEntity : Identifiable {

}
