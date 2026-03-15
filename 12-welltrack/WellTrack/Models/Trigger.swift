//
//  Trigger.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/19/23.
//

import Foundation
import CoreData



class Trigger: NSManagedObject {
    @NSManaged var id: UUID
    @NSManaged public var active: Bool
    @NSManaged public var title: String
    @NSManaged public var childInputs: NSSet?
    @NSManaged public var actionState: ActionState
    @NSManaged public var systemImage: String
    @NSManaged public var dateUpdated: Date
    
    override func awakeFromInsert() {
        super.awakeFromInsert()
        
        setPrimitiveValue(UUID(), forKey: "id")
        setPrimitiveValue(Date.now, forKey: "dateUpdated")
    }
}




final class TriggerButton: Trigger {
    @NSManaged public var buttonText: String?
}



//final class DateTrigger: Trigger {
//    @NSManaged public var date: Date?
//    @NSManaged public var time: Date?
//}
