//
//  ManualInputEntity+CoreDataProperties.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/25/23.
//
//

import Foundation
import CoreData


extension ManualInputEntity {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<ManualInputEntity> {
        return NSFetchRequest<ManualInputEntity>(entityName: "ManualInputEntity")
    }

    @NSManaged public var booleanValue: Bool
    @NSManaged public var dateValue: Date?
    @NSManaged public var id: UUID?
    @NSManaged public var inputType: String?
    @NSManaged public var numberValue: Double
    @NSManaged public var prompt: String?
    @NSManaged public var timeValue: Date?
    @NSManaged public var actionState: ActionStateEntity?
    @NSManaged public var list: ListEntity?

}

extension ManualInputEntity : Identifiable {

}
