//
//  FieldVariableEntity+CoreDataProperties.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//
//

import Foundation
import CoreData


extension FieldVariableEntity {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<FieldVariableEntity> {
        return NSFetchRequest<FieldVariableEntity>(entityName: "FieldVariableEntity")
    }

    @NSManaged public var id: UUID?
    @NSManaged public var value: String?
    @NSManaged public var variable: String?
    @NSManaged public var field: FieldEntity?

}

extension FieldVariableEntity : Identifiable {

}

