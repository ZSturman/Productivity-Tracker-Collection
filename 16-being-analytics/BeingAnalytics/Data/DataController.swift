//
//  DataController.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/2/23.
//

import Foundation
import CoreData

final class DataController {
    
    static let shared = DataController()
    
    private let persistentContainer: NSPersistentContainer
    
    var viewContext: NSManagedObjectContext {
        persistentContainer.viewContext
    }
    
    var newContext: NSManagedObjectContext {
        persistentContainer.newBackgroundContext()
    }
    
    private init(){
        print("Initializing DataController...")
        persistentContainer = NSPersistentContainer(name: "BeingAnalyticsCoreData")
        persistentContainer.viewContext.automaticallyMergesChangesFromParent = true
        persistentContainer.loadPersistentStores { _, error in
            if let error {
                print("Error loading persistent stores: \(error)")
                fatalError("Unable to load store with error: \(error)")
            } else {
                print("Persistent stores loaded successfully.")
            }
        }
    }
    
    func saveChanges(in context: NSManagedObjectContext) throws {
        print("Attempting to save changes...")
        if context.hasChanges {
            do {
                try context.save()
                print("Changes saved successfully.")
            } catch let error as NSError {
                print("Error saving changes: \(error), \(error.userInfo)")
            }
        } else {
            print("No changes to save.")
        }
    }
}
