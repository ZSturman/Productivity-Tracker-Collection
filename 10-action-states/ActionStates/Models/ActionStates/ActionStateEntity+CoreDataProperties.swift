//
//  ActionStateEntity+CoreDataProperties.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/25/23.
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
    @NSManaged public var latitude: Double
    @NSManaged public var longitude: Double
    @NSManaged public var name: String?
    @NSManaged public var timestamp: Date?
    @NSManaged public var type: String?
    @NSManaged public var manualInputs: NSSet?
    @NSManaged public var tags: NSSet?
    @NSManaged public var topic: NSSet?

}

// MARK: Generated accessors for manualInputs
extension ActionStateEntity {

    @objc(addManualInputsObject:)
    @NSManaged public func addToManualInputs(_ value: ManualInputEntity)

    @objc(removeManualInputsObject:)
    @NSManaged public func removeFromManualInputs(_ value: ManualInputEntity)

    @objc(addManualInputs:)
    @NSManaged public func addToManualInputs(_ values: NSSet)

    @objc(removeManualInputs:)
    @NSManaged public func removeFromManualInputs(_ values: NSSet)

}

// MARK: Generated accessors for tags
extension ActionStateEntity {

    @objc(addTagsObject:)
    @NSManaged public func addToTags(_ value: TagEntity)

    @objc(removeTagsObject:)
    @NSManaged public func removeFromTags(_ value: TagEntity)

    @objc(addTags:)
    @NSManaged public func addToTags(_ values: NSSet)

    @objc(removeTags:)
    @NSManaged public func removeFromTags(_ values: NSSet)

}

// MARK: Generated accessors for topic
extension ActionStateEntity {

    @objc(addTopicObject:)
    @NSManaged public func addToTopic(_ value: TopicEntity)

    @objc(removeTopicObject:)
    @NSManaged public func removeFromTopic(_ value: TopicEntity)

    @objc(addTopic:)
    @NSManaged public func addToTopic(_ values: NSSet)

    @objc(removeTopic:)
    @NSManaged public func removeFromTopic(_ values: NSSet)

}

extension ActionStateEntity : Identifiable {

}
