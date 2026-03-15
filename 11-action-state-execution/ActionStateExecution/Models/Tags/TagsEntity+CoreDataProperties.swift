//
//  TagsEntity+CoreDataProperties.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//
//

import Foundation
import CoreData


extension TagsEntity {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<TagsEntity> {
        return NSFetchRequest<TagsEntity>(entityName: "TagsEntity")
    }

    @NSManaged public var id: UUID?
    @NSManaged public var name: String?
    @NSManaged public var actionStates: NSSet?

}

// MARK: Generated accessors for actionStates
extension TagsEntity {

    @objc(addActionStatesObject:)
    @NSManaged public func addToActionStates(_ value: ActionStateEntity)

    @objc(removeActionStatesObject:)
    @NSManaged public func removeFromActionStates(_ value: ActionStateEntity)

    @objc(addActionStates:)
    @NSManaged public func addToActionStates(_ values: NSSet)

    @objc(removeActionStates:)
    @NSManaged public func removeFromActionStates(_ values: NSSet)

}

extension TagsEntity : Identifiable {

}
