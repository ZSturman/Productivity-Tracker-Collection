//
//  DataController.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation
import CoreData
import SwiftUI

final class DataController {
    
    static let shared = DataController()
    
    private let persistentContainer: NSPersistentContainer
    
    var viewContext: NSManagedObjectContext {
        persistentContainer.viewContext
    }
    
    private(set) var backgroundContext: NSManagedObjectContext
    
    var newContext: NSManagedObjectContext {
        backgroundContext
    }
    
    private init(){
        persistentContainer = NSPersistentContainer(name: "TrackingWellCoreData")
        
        if EnvironmentValues.isPreview || Thread.current.isRunningXCTest {
            persistentContainer.persistentStoreDescriptions.first?.url = .init(fileURLWithPath: "/dev/null")
        }
        
        persistentContainer.viewContext.automaticallyMergesChangesFromParent = true
        persistentContainer.loadPersistentStores { _, error in
            if let error = error {
                fatalError("Unable to load store with error: \(error)")
            }
        }
        
        backgroundContext = persistentContainer.newBackgroundContext()
    }
    
    func exists<T: NSManagedObject>(_ object: T, in context: NSManagedObjectContext) -> T? {
        try? context.existingObject(with: object.objectID) as? T
    }
    
    func delete<T: NSManagedObject>(_ object: T, in context: NSManagedObjectContext) throws {
        if let existingObject = exists(object, in: context) {
            context.delete(existingObject)
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

extension DataController {
    // Sample factory methods for creating entities. Repeat for other entities as needed.

    func createActionState(in context: NSManagedObjectContext) -> ActionState {
        return ActionState(context: context)
    }

    func createTrigger(in context: NSManagedObjectContext) -> Trigger {
        return Trigger(context: context)
    }

    func createInput(in context: NSManagedObjectContext) -> Input {
        return Input(context: context)
    }

    func createExecution(in context: NSManagedObjectContext) -> Execution {
        return Execution(context: context)
    }

    func createInputExecution(in context: NSManagedObjectContext) -> InputExecution {
        return InputExecution(context: context)
    }
}

extension EnvironmentValues {
    static var isPreview: Bool {
        return ProcessInfo.processInfo.environment["XCODE_RUNNING_FOR_PREVIEWS"] == "1"
    }
}

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
