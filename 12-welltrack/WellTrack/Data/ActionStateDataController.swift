//
//  ActionStateDataController.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/15/23.
//

import Foundation
import CoreData
import SwiftUI

final class ActionStateDataController {
    
    static let shared = ActionStateDataController()
    
    private let persistentContainer: NSPersistentContainer
    
    var viewContext: NSManagedObjectContext {
        persistentContainer.viewContext
    }
    
    var newContext: NSManagedObjectContext {
        persistentContainer.newBackgroundContext()
    }
    
    private init(){
        persistentContainer = NSPersistentContainer(name: "ActionStateCoreData")
        if EnvironmentValues.isPreview || Thread.current.isRunningXCTest {
            persistentContainer.persistentStoreDescriptions.first?.url = .init(fileURLWithPath: "/dev/null")
        }
        // For saving changes when we commit it
        persistentContainer.viewContext.automaticallyMergesChangesFromParent = true
        persistentContainer.loadPersistentStores { _, error in
            if let error {
                fatalError("Unable to load store with error: \(error)")
            }
        }
    }
    
    func exists(_ actionState: ActionState, in context: NSManagedObjectContext) -> ActionState? {
        try? context.existingObject(with: actionState.objectID) as? ActionState
    }
    
    func delete(_ actionState: ActionState, in context: NSManagedObjectContext) throws {
        if let existingActionState = exists(actionState, in: context) {
            context.delete(existingActionState)
            Task(priority: .background) {
                try await context.perform {
                    try context.save()
                }
            }
        }
    }
    
    func saveChanges(in context: NSManagedObjectContext) throws {
        if context.hasChanges {
            try context.save()
        }
    }
}





extension ActionStateDataController {
    
    func askForTextInput(in context: NSManagedObjectContext) -> AskForTextInput {
        return AskForTextInput(context: context)
    }

    func askForNumberInput(in context: NSManagedObjectContext) -> AskForNumberInput {
        return AskForNumberInput(context: context)
    }
    
    func setTextInput(in context: NSManagedObjectContext) -> SetTextInput {
        return SetTextInput(context: context)
    }
    
    func setNumberInput(in context: NSManagedObjectContext) -> SetNumberInput {
        return SetNumberInput(context: context)
    }
    
    func calculateInput(in context: NSManagedObjectContext) -> CalculateInput {
        return CalculateInput(context: context)
    }
    
    
    func createTriggerButton(in context: NSManagedObjectContext) -> TriggerButton {
        return TriggerButton(context: context)
    }
    
    func executeStringOutput(in context: NSManagedObjectContext) -> ExecutionString {
        return ExecutionString(context: context)
    }
    
    func executeNumberOutput(in context: NSManagedObjectContext) -> ExecutionNumber {
        return ExecutionNumber(context: context)
    }
    
    
    

}







extension EnvironmentValues {
    static var isPreview: Bool {
        return ProcessInfo.processInfo.environment["XCODE_RUNNING_FOR_PREVIEWS"] == "1"
    }
}

// For Testing
extension Thread {
    var isRunningXCTest: Bool {
        for key in self.threadDictionary.allKeys {
            guard let keyAsString = key as? String else {
                continue
            }
            
            if keyAsString.split(separator: ".").contains("xctest") {
                return true
            }
        }
        return false
    }
}
