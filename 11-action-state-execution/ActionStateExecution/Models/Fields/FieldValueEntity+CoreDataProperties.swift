//
//  FieldValueEntity+CoreDataProperties.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//
//

import Foundation
import CoreData


extension FieldValueEntity {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<FieldValueEntity> {
        return NSFetchRequest<FieldValueEntity>(entityName: "FieldValueEntity")
    }

    @NSManaged public var id: UUID?
    @NSManaged public var value: String?
    @NSManaged public var executionID: ExecutionEntity?
    @NSManaged public var fieldID: FieldEntity?
    @NSManaged public var listItems: NSSet?

}

// MARK: Generated accessors for listItems
extension FieldValueEntity {

    @objc(addListItemsObject:)
    @NSManaged public func addToListItems(_ value: ListItemEntity)

    @objc(removeListItemsObject:)
    @NSManaged public func removeFromListItems(_ value: ListItemEntity)

    @objc(addListItems:)
    @NSManaged public func addToListItems(_ values: NSSet)

    @objc(removeListItems:)
    @NSManaged public func removeFromListItems(_ values: NSSet)

}

extension FieldValueEntity : Identifiable {

}
