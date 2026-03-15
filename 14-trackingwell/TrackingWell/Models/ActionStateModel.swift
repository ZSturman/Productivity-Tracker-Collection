//
//  ActionStateModel.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation
import CoreData


extension ActionState {

    // Fetch Request for all ActionStates
    private static var actionStateFetchRequest: NSFetchRequest<ActionState> {
        NSFetchRequest(entityName: "ActionState")
    }

    // Fetch all ActionStates with default sort order
    static func all() -> NSFetchRequest<ActionState> {
        let request: NSFetchRequest<ActionState> = actionStateFetchRequest
        request.sortDescriptors = [
            NSSortDescriptor(keyPath: \ActionState.dateUpdated, ascending: false)
        ]
        return request
    }

    // Filter based on SearchConfig
    static func filter(with config: SearchConfig) -> NSPredicate {
        switch config.filter {
        case .all:
            return config.query.isEmpty
                ? NSPredicate(value: true)
                : NSPredicate(format: "title CONTAINS[cd] %@", config.query)
        case .action:
            if config.query.isEmpty {
                return NSPredicate(format: "isAction == %@", NSNumber(value: true))
            } else {
                return NSCompoundPredicate(andPredicateWithSubpredicates: [
                    NSPredicate(format: "title CONTAINS[cd] %@", config.query),
                    NSPredicate(format: "isAction == %@", NSNumber(value: true))
                ])
            }
        case .state:
            if config.query.isEmpty {
                return NSPredicate(format: "isAction == %@", NSNumber(value: false))
            } else {
                return NSCompoundPredicate(andPredicateWithSubpredicates: [
                    NSPredicate(format: "title CONTAINS[cd] %@", config.query),
                    NSPredicate(format: "isAction == %@", NSNumber(value: false))
                ])
            }
        }
    }


    // Sort based on Sort order
    static func sort(order: Sort) -> [NSSortDescriptor] {
        [NSSortDescriptor(keyPath: \ActionState.dateUpdated, ascending: order == .asc)]
    }
}

