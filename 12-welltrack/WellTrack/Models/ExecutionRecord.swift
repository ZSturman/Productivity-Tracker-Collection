//
//  ExecutionRecord.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/19/23.
//


import Foundation
import CoreData

class ExecutionRecord: NSManagedObject {
    @NSManaged var id: UUID
    @NSManaged var timestamp: Date
    @NSManaged var actionState: ActionState
    @NSManaged var executionOutput: Input
    
    override func awakeFromInsert() {
        super.awakeFromInsert()
        
        setPrimitiveValue(UUID(), forKey: "id")
        setPrimitiveValue(Date.now, forKey: "timestamp")
    }
    
}

final class ExecutionString: ExecutionRecord {
    @NSManaged var outputValue: String
    
//    func convertToString(outputValue: ) -> ExecutionRecord {
//        convert Number to String for easy output
//
//    }
}

final class ExecutionNumber: ExecutionRecord {
    @NSManaged var outputValue: Double
}


