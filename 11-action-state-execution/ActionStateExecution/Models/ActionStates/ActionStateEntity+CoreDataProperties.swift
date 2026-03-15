//
//  ActionStateEntity+CoreDataProperties.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//
//

import Foundation
import CoreData


extension ActionStateEntity {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<ActionStateEntity> {
        return NSFetchRequest<ActionStateEntity>(entityName: "ActionStateEntity")
    }

    @NSManaged public var collectDate: Bool
    @NSManaged public var collectLocation: Bool
    @NSManaged public var collectTime: Bool
    @NSManaged public var explanation: String?
    @NSManaged public var id: UUID?
    @NSManaged public var name: String?
    @NSManaged public var category: String?
    @NSManaged public var executions: NSSet?
    @NSManaged public var fields: NSSet?
    @NSManaged public var tags: NSSet?
    @NSManaged public var topic: TopicsEntity?

}

// MARK: Generated accessors for executions
extension ActionStateEntity {

    @objc(addExecutionsObject:)
    @NSManaged public func addToExecutions(_ value: ExecutionEntity)

    @objc(removeExecutionsObject:)
    @NSManaged public func removeFromExecutions(_ value: ExecutionEntity)

    @objc(addExecutions:)
    @NSManaged public func addToExecutions(_ values: NSSet)

    @objc(removeExecutions:)
    @NSManaged public func removeFromExecutions(_ values: NSSet)

}

// MARK: Generated accessors for fields
extension ActionStateEntity {

    @objc(addFieldsObject:)
    @NSManaged public func addToFields(_ value: FieldEntity)

    @objc(removeFieldsObject:)
    @NSManaged public func removeFromFields(_ value: FieldEntity)

    @objc(addFields:)
    @NSManaged public func addToFields(_ values: NSSet)

    @objc(removeFields:)
    @NSManaged public func removeFromFields(_ values: NSSet)

}

// MARK: Generated accessors for tags
extension ActionStateEntity {

    @objc(addTagsObject:)
    @NSManaged public func addToTags(_ value: TagsEntity)

    @objc(removeTagsObject:)
    @NSManaged public func removeFromTags(_ value: TagsEntity)

    @objc(addTags:)
    @NSManaged public func addToTags(_ values: NSSet)

    @objc(removeTags:)
    @NSManaged public func removeFromTags(_ values: NSSet)

}

extension ActionStateEntity : Identifiable {

}
