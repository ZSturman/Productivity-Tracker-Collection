//
//  ExecutionDetailViewModel.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation

class ExecutionDetailViewModel: ObservableObject {
    @Published var execution: Execution

    var executionDetailInfo: String {
        // Convert execution details to a displayable string format
        return "\(execution.timestamp)"
    }

    init(execution: Execution) {
        self.execution = execution
        fetchExecutionDetails()
    }

    func fetchExecutionDetails() {
        // Fetch additional details for the given execution if needed
    }
}
