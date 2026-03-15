//
//  ExecutionListViewModel.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation

class ExecutionListViewModel: ObservableObject {
    @Published var executions: [Execution] = []

    init(actionState: ActionState) {
        fetchExecutionsForActionState(actionState: actionState)
    }

    func fetchExecutionsForActionState(actionState: ActionState) {
        // Fetch logic to get all executions related to the given actionState from CoreData
        // Update executions property
    }

    func sortAndFilter() {
        // Implement sort and filter logic for executions
    }
}
