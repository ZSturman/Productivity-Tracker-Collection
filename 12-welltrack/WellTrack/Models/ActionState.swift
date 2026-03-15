//
//  ActionState.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/15/23.
//

import Foundation
import CoreData



final class ActionState: NSManagedObject, Identifiable {
    
    @NSManaged var title: String
    @NSManaged var category: String
    @NSManaged var dateCreated: Date
    @NSManaged var dateUpdated: Date
    @NSManaged var collectLocation: Bool
    @NSManaged var inputs: NSSet
    @NSManaged var triggers: NSSet
    @NSManaged var executionRecords: NSSet

    var isValid: Bool {
        !title.isEmpty
    }

    override func awakeFromInsert() {
        super.awakeFromInsert()

        setPrimitiveValue(Date.now, forKey: "dateCreated")
        setPrimitiveValue(Date.now, forKey: "dateUpdated")
        setPrimitiveValue(true, forKey: "collectLocation")
    }
}


// EXECUTIONS
extension ActionState {
    func addToExecutionRecords(_ value: ExecutionRecord) {
        let items = self.mutableSetValue(forKey: "executionRecords")
        items.add(value)
    }
    
    func removeFromExecutionRecords(_ value: ExecutionRecord) {
        let items = self.mutableSetValue(forKey: "executionRecords")
        items.remove(value)
    }

    
}



// For Filtering and Fetching
extension ActionState {
    
    private static var actionStateFetchRequest: NSFetchRequest<ActionState> {
        NSFetchRequest(entityName: "ActionState")
    }
    
    static func all() -> NSFetchRequest<ActionState> {
        let request: NSFetchRequest<ActionState> = actionStateFetchRequest
        request.sortDescriptors = [
            NSSortDescriptor(keyPath: \ActionState.dateUpdated, ascending: false)
        ]
        return request
    }
    
    
    static func filter(with config: SearchConfig) -> NSPredicate {
        switch config.filter {
            case .all:
                return config.query.isEmpty
                    ? NSPredicate(value: true)
                    : NSPredicate(format: "title CONTAINS[cd] %@", config.query)
            
            case .action:
                if config.query.isEmpty {
                    return NSPredicate(format: "category == %@", "Action")
                } else {
                    return NSCompoundPredicate(andPredicateWithSubpredicates: [
                        NSPredicate(format: "title CONTAINS[cd] %@", config.query),
                        NSPredicate(format: "category == %@", "Action")
                    ])
                }
            case .state:
                if config.query.isEmpty {
                    return NSPredicate(format: "category == %@", "State")
                } else {
                    return NSCompoundPredicate(andPredicateWithSubpredicates: [
                        NSPredicate(format: "title CONTAINS[cd] %@", config.query),
                        NSPredicate(format: "category == %@", "State")
                    ])
                }
        }
    }
    
    static func sort(order: Sort) -> [NSSortDescriptor] {
        [NSSortDescriptor(keyPath: \ActionState.dateUpdated, ascending: order == .asc)]
    }
}



// FOR PREVIEWS
extension ActionState {
    @discardableResult
    static func makePreview(count: Int, in context: NSManagedObjectContext) -> [ActionState] {
        var actionStates = [ActionState]()
        for i in 0..<count {
            let actionState = ActionState(context: context)
            actionState.title = "ActionState \(i)"
            actionState.collectLocation = Bool.random()
            actionState.category = Bool.random() ? "Action" : "State"
            actionState.dateCreated = Calendar.current.date(byAdding: .day, value: -i, to: .now) ?? .now
            actionState.dateUpdated = Calendar.current.date(byAdding: .day, value: -i, to: .now) ?? .now

            actionStates.append(actionState)
        }
        return actionStates
    }

    
    static func preview(context: NSManagedObjectContext = ActionStateDataController.shared.viewContext) -> ActionState {
        return makePreview(count: 1, in: context)[0]
    }
    
    static func empty(context: NSManagedObjectContext = ActionStateDataController.shared.viewContext) -> ActionState {
        return ActionState(context: context)
    }
}
