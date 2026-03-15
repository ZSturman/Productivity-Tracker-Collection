//
//  TopicEntity+CoreDataProperties.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/25/23.
//
//

import Foundation
import CoreData


extension TopicEntity {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<TopicEntity> {
        return NSFetchRequest<TopicEntity>(entityName: "TopicEntity")
    }

    @NSManaged public var id: UUID?
    @NSManaged public var name: String?
    @NSManaged public var topicDescription: String?
    @NSManaged public var actionStates: NSSet?

}

// MARK: Generated accessors for actionStates
extension TopicEntity {

    @objc(addActionStatesObject:)
    @NSManaged public func addToActionStates(_ value: ActionStateEntity)

    @objc(removeActionStatesObject:)
    @NSManaged public func removeFromActionStates(_ value: ActionStateEntity)

    @objc(addActionStates:)
    @NSManaged public func addToActionStates(_ values: NSSet)

    @objc(removeActionStates:)
    @NSManaged public func removeFromActionStates(_ values: NSSet)

}

extension TopicEntity : Identifiable {

}
