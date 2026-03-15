//
//  ExecutionEntity+CoreDataProperties.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//
//

import Foundation
import CoreData


extension ExecutionEntity {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<ExecutionEntity> {
        return NSFetchRequest<ExecutionEntity>(entityName: "ExecutionEntity")
    }

    @NSManaged public var id: UUID?
    @NSManaged public var timestamp: Date?
    @NSManaged public var latitude: Double
    @NSManaged public var longitude: Double
    @NSManaged public var actionStateID: ActionStateEntity?
    @NSManaged public var fieldValues: NSSet?

}

// MARK: Generated accessors for fieldValues
extension ExecutionEntity {

    @objc(addFieldValuesObject:)
    @NSManaged public func addToFieldValues(_ value: FieldValueEntity)

    @objc(removeFieldValuesObject:)
    @NSManaged public func removeFromFieldValues(_ value: FieldValueEntity)

    @objc(addFieldValues:)
    @NSManaged public func addToFieldValues(_ values: NSSet)

    @objc(removeFieldValues:)
    @NSManaged public func removeFromFieldValues(_ values: NSSet)

}

extension ExecutionEntity : Identifiable {

}
