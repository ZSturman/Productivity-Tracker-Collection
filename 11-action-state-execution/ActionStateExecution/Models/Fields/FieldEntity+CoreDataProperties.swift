//
//  FieldEntity+CoreDataProperties.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/2/23.
//
//

import Foundation
import CoreData


extension FieldEntity {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<FieldEntity> {
        return NSFetchRequest<FieldEntity>(entityName: "FieldEntity")
    }

    @NSManaged public var fieldName: String?
    @NSManaged public var fieldType: String?
    @NSManaged public var id: UUID?
    @NSManaged public var order: Int16
    @NSManaged public var prompt: String?
    @NSManaged public var actionState: ActionStateEntity?
    @NSManaged public var fieldValues: NSSet?
    @NSManaged public var fieldVars: NSSet?
    @NSManaged public var list: ListEntity?

}

// MARK: Generated accessors for fieldValues
extension FieldEntity {

    @objc(addFieldValuesObject:)
    @NSManaged public func addToFieldValues(_ value: FieldValueEntity)

    @objc(removeFieldValuesObject:)
    @NSManaged public func removeFromFieldValues(_ value: FieldValueEntity)

    @objc(addFieldValues:)
    @NSManaged public func addToFieldValues(_ values: NSSet)

    @objc(removeFieldValues:)
    @NSManaged public func removeFromFieldValues(_ values: NSSet)

}

// MARK: Generated accessors for fieldVars
extension FieldEntity {

    @objc(addFieldVarsObject:)
    @NSManaged public func addToFieldVars(_ value: FieldVariableEntity)

    @objc(removeFieldVarsObject:)
    @NSManaged public func removeFromFieldVars(_ value: FieldVariableEntity)

    @objc(addFieldVars:)
    @NSManaged public func addToFieldVars(_ values: NSSet)

    @objc(removeFieldVars:)
    @NSManaged public func removeFromFieldVars(_ values: NSSet)

}

extension FieldEntity : Identifiable {

}
