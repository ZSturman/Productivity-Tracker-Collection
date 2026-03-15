//
//  DataController.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/22/23.
//

import CoreData
import Foundation

class DataController: ObservableObject {
    let container: NSPersistentContainer
    
    init() {
        container = NSPersistentContainer(name: "ActionStatesData")
        container.loadPersistentStores { description, error in
            if let error = error {
                print("Core Data failed to load: \(error.localizedDescription)")
                return
            }
        }
    }
    
}
