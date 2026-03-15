//
//  TempActionState.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//
import CoreData
import SwiftUI

// MARK: - TempActionState Definition
struct TempActionState {
    var id: UUID
    var dateCreated: Date
    var dateUpdated: Date
    var title: String
    var isAction: Bool
    var triggers: [TempTrigger]
    var executions: [TempExecution]

    // Default initializer for creating a new TempActionState with default values
    init(id: UUID = UUID(),
         dateCreated: Date = Date(),
         dateUpdated: Date = Date(),
         title: String = "",
         isAction: Bool = true,
         triggers: [TempTrigger] = [],
         executions: [TempExecution] = []) {
        self.id = id
        self.dateCreated = dateCreated
        self.dateUpdated = dateUpdated
        self.title = title
        self.isAction = isAction
        self.triggers = triggers
        self.executions = executions
    }
}

// MARK: - Initializing TempActionState from ActionState
extension TempActionState {
    // Initialize TempActionState from an existing CoreData ActionState object
    init(from actionState: ActionState, in context: NSManagedObjectContext) {
        // Handle optional properties and provide default values if nil
        self.id = actionState.id ?? UUID()
        self.dateCreated = actionState.dateCreated ?? Date()
        self.dateUpdated = actionState.dateUpdated ?? Date()
        self.title = actionState.title ?? ""
        self.isAction = actionState.isAction
        
        // Convert the triggers and executions sets to TempTrigger and TempExecution arrays
        self.triggers = (actionState.triggers as? Set<Trigger>).map { $0.map { TempTrigger(from: $0, in: context) } } ?? []
        self.executions = (actionState.executions as? Set<Execution>).map { $0.map { TempExecution(from: $0, in: context) } } ?? []
    }
}

// MARK: - Initializing ActionState from TempActionState
extension ActionState {
    // Initialize CoreData ActionState object from a TempActionState object
    convenience init(from tempObject: TempActionState, in context: NSManagedObjectContext) {
        // Retrieve the entity description for ActionState and initialize
        let entity = NSEntityDescription.entity(forEntityName: "ActionState", in: context)!
        self.init(entity: entity, insertInto: context)
        
        // Assign properties from the temporary object
        self.id = tempObject.id
        self.dateCreated = tempObject.dateCreated
        self.dateUpdated = tempObject.dateUpdated
        self.title = tempObject.title
        self.isAction = tempObject.isAction
        
        // Convert TempTrigger and TempExecution arrays to NSSet and assign to relationships
        self.addToTriggers(NSSet(array: tempObject.triggers.map { Trigger(from: $0, in: context) }))
        self.addToExecutions(NSSet(array: tempObject.executions.map { Execution(from: $0, in: context) }))
    }
}


// MARK: - Update ActionState
extension ActionState {
    // Update the properties of ActionState with the values from TempActionState
    func update(from tempObject: TempActionState, in context: NSManagedObjectContext) {
        // Check if the values are different and update them accordingly
        if self.id != tempObject.id {
            self.id = tempObject.id
        }
        
        if self.title != tempObject.title {
            self.title = tempObject.title
        }
        
        if self.isAction != tempObject.isAction {
            self.isAction = tempObject.isAction
        }
        
        
        
        // Convert TempTrigger and TempExecution arrays to NSSet and update the relationships
        let newTriggers = NSSet(array: tempObject.triggers.map { Trigger(from: $0, in: context) })
        if self.triggers != newTriggers {
            self.removeFromTriggers(self.triggers ?? NSSet())
            self.addToTriggers(newTriggers)
        }
        
        
        let newExecutions = NSSet(array: tempObject.executions.map { Execution(from: $0, in: context) })
        if self.executions != newExecutions {
            self.removeFromExecutions(self.executions ?? NSSet())
            self.addToExecutions(newExecutions)
        }
        
        self.dateUpdated = Date()
    }
}

