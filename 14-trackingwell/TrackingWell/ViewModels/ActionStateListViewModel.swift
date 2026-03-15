//
//  ActionStateListViewModel.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation
import CoreData

class ActionStateListViewModel: ObservableObject {
    @Published var actionStates: [ActionState] = []
    
    // Search and Sort Configurations
    @Published var searchConfig: SearchConfig = .init()
    @Published var sort: Sort = .desc

    private var dataController: DataController
    private var fetchedResultsController: NSFetchedResultsController<ActionState>

    init(dataController: DataController = DataController.shared) {
        self.dataController = dataController
        
        let fetchRequest: NSFetchRequest<ActionState> = ActionState.all()
        fetchedResultsController = NSFetchedResultsController(
            fetchRequest: fetchRequest,
            managedObjectContext: dataController.viewContext,
            sectionNameKeyPath: nil,
            cacheName: nil
        )

        fetchActionStates()
    }
    
//    func fetchActionStates() {
//        let fetchRequest: NSFetchRequest<ActionState> = ActionState.fetchRequest()
//        do {
//            actionStates = try viewContext.fetch(fetchRequest)
//        } catch {
//            print("Failed to fetch ActionStates: \(error)")
//        }
//    }


    func fetchActionStates() {
        fetchedResultsController.fetchRequest.predicate = ActionState.filter(with: searchConfig)
        fetchedResultsController.fetchRequest.sortDescriptors = ActionState.sort(order: sort)

        do {
            try fetchedResultsController.performFetch()
            actionStates = fetchedResultsController.fetchedObjects ?? []
        } catch {
            print("Failed to fetch ActionStates with error: \(error)")
        }
    }

    // Call this whenever searchConfig or sort changes
    func updateActionStates() {
        fetchActionStates()
    }
}
