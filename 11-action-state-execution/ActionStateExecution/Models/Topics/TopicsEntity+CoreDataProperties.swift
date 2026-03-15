//
//  TopicsEntity+CoreDataProperties.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//
//

import Foundation
import CoreData


extension TopicsEntity {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<TopicsEntity> {
        return NSFetchRequest<TopicsEntity>(entityName: "TopicsEntity")
    }

    @NSManaged public var explanation: String?
    @NSManaged public var id: UUID?
    @NSManaged public var name: String?
    @NSManaged public var actionStates: ActionStateEntity?

}

extension TopicsEntity : Identifiable {

}
