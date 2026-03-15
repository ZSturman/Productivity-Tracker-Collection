//
//  ListEntity+CoreDataProperties.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/27/23.
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
    @NSManaged public var manualInputs: NSSet?

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

// MARK: Generated accessors for manualInputs
extension ListEntity {

    @objc(addManualInputsObject:)
    @NSManaged public func addToManualInputs(_ value: ManualInputEntity)

    @objc(removeManualInputsObject:)
    @NSManaged public func removeFromManualInputs(_ value: ManualInputEntity)

    @objc(addManualInputs:)
    @NSManaged public func addToManualInputs(_ values: NSSet)

    @objc(removeManualInputs:)
    @NSManaged public func removeFromManualInputs(_ values: NSSet)

}

extension ListEntity : Identifiable {

}
