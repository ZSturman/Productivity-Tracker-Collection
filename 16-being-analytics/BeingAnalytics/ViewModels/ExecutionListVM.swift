//
//  ExecutionListVM.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/4/23.
//

import Foundation

class ExecutionListVM: ObservableObject {
    var dataService: DataService
    var actionState: ActionState

    @Published var executions: [Execution]
    @Published var groupedExecutions: [Date: [Execution]] = [:]
    
    init(dataService: DataService, actionState: ActionState) {
        self.dataService = dataService
        self.actionState = actionState
        
        if let actionStateID = actionState.id {
            self.executions = dataService.fetchExecutionsByActionStateID(actionStateID: actionStateID)
            updateGroupedExecutions()
        } else {
            self.executions = []
            print("Warning: actionState.id is nil!")
        }
    }
    
    func updateGroupedExecutions() {
        let sortedExecutions = self.executions.sorted(by: { ($0.timestamp ?? Date.distantPast) < ($1.timestamp ?? Date.distantPast) })
        
        for execution in sortedExecutions {
            if let executionDate = execution.timestamp {
                let calendar = Calendar.current
                let dateComponents = calendar.dateComponents([.year, .month, .day], from: executionDate)
                if let date = calendar.date(from: dateComponents) {
                    if groupedExecutions[date] == nil {
                        groupedExecutions[date] = [execution]
                    } else {
                        groupedExecutions[date]?.append(execution)
                    }
                }
            }
        }
    }
}
