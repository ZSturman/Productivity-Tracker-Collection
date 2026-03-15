//
//  ActionStateListVM.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import Foundation
import SwiftUI

class ActionStateListVM: ObservableObject {
    var dataService: DataService
    
    @Published var actionStates: [ActionState]
    @Published var executions: [Execution] = []
    
    @Published var searchConfig: SearchConfig = .init()
    @Published var sort: Sort = .desc

    
    init(dataService: DataService) {
        self.dataService = dataService
        self.actionStates = dataService.fetchAllActionStates()

        NotificationCenter.default.addObserver(self, selector: #selector(refreshActionStates), name: .newActionStateSaved, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(refreshActionStates), name: .actionStateUpdated, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(refreshActionStates), name: .deletedActionState, object: nil)

    }
    
    
    func filterAndSortActionStates() {
        var filteredActionStates = dataService.fetchAllActionStates()

        // Filtering based on query
        if !searchConfig.query.isEmpty {
            filteredActionStates = filteredActionStates.filter {
                $0.title?.contains(searchConfig.query) ?? false
            }
        }


        // Further filtering based on the filter type
        switch searchConfig.filter {
        case .action:
            filteredActionStates = filteredActionStates.filter {
                $0.isAction
            }
        case .state:
            filteredActionStates = filteredActionStates.filter {
                !$0.isAction
            }
        case .all:
            break
        }

        // Sorting
        switch sort {
        case .asc:
            filteredActionStates.sort {
                ($0.dateUpdated ?? Date()) < ($1.dateUpdated ?? Date())
            }
        case .desc:
            filteredActionStates.sort {
                ($0.dateUpdated ?? Date()) > ($1.dateUpdated ?? Date())
            }
        }

        self.actionStates = filteredActionStates
    }


    
    
    

    @objc func refreshActionStates() {
        self.actionStates = dataService.fetchAllActionStates()
        filterAndSortActionStates()
    }

    
    func fetchExecutionsForActionState(actionStateID: UUID) {
        self.executions = dataService.fetchExecutionsByActionStateID(actionStateID: actionStateID)
    }
    
    deinit {
        NotificationCenter.default.removeObserver(self)
    }


    
}

