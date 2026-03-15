//
//  ListItemEntity+CoreDataProperties.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/27/23.
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
    
    public var wrappedName: String {
        name ?? "Unknown Item"
    }

}

extension ListItemEntity : Identifiable {

}
