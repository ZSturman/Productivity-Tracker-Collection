//
//  TempExecution.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import CoreData
import SwiftUI

struct TempExecution {
    var id: UUID
    var outputValue: String
    var timestamp: Date
    var actionStateID: UUID
    var inputExecutions: [TempInputExecution]
    
    var inputCalculations: [TempInputCalculationExecution] = []
    
    init(id: UUID = UUID(),
         outputValue: String = "Default Output",
         timestamp: Date = Date(),
         actionStateID: UUID = UUID(),
         inputExecutions: [TempInputExecution] = []) {
        self.id = id
        self.outputValue = outputValue
        self.timestamp = timestamp
        self.actionStateID = actionStateID
        self.inputExecutions = inputExecutions
    }
}


struct TempInputCalculationExecution {
    var calculateInputID: UUID?
    var valueOneInputExecution: UUID?
    var valueTwoInputExecution: UUID?
    
}

// MARK: - Initializing TempExecution from Execution
extension TempExecution {
    init(from execution: Execution, in context: NSManagedObjectContext) {
        // Initialize properties using values from the Execution object
        self.id = execution.id ?? UUID()
        self.outputValue = execution.outputValue ?? ""
        self.timestamp = execution.timestamp ?? Date()
        self.actionStateID = execution.actionState?.id ?? UUID()
        
        // Convert the inputExecutions set to TempInputExecution array
        self.inputExecutions = (execution.inputExecutions as? Set<InputExecution>).map { $0.map { TempInputExecution(from: $0) } } ?? []
    }
}

// MARK: - Initializing Execution from TempExecution
extension Execution {
    convenience init(from tempObject: TempExecution, in context: NSManagedObjectContext) {
        let entity = NSEntityDescription.entity(forEntityName: "Execution", in: context)!
        self.init(entity: entity, insertInto: context)
        
        // Set properties using values from the temporary object
        self.id = tempObject.id
        self.outputValue = tempObject.outputValue
        self.timestamp = tempObject.timestamp
        
//        // If ActionState with the given ID exists in context, set the relationship
//        if let actionState = try? context.existingObject(with: NSManagedObjectID(for: tempObject.actionStateID)) as? ActionState {
//            self.actionState = actionState
//        }
        
        let inputExecutions = tempObject.inputExecutions.compactMap { InputExecution.create(from: $0, in: context) }
        self.addToInputExecutions(NSSet(array: inputExecutions))
    }
}
