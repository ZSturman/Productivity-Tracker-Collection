//
//  ListItemEntity+CoreDataProperties.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//
//

import Foundation
import CoreData


extension ListItemEntity {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<ListItemEntity> {
        return NSFetchRequest<ListItemEntity>(entityName: "ListItemEntity")
    }

    @NSManaged public var id: UUID?
    @NSManaged public var name: String?
    @NSManaged public var list: ListEntity?
    @NSManaged public var fieldValues: FieldValueEntity?

}

extension ListItemEntity : Identifiable {

}
