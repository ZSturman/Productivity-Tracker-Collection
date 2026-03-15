//
//  TriggerViewModel.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation

class TriggerViewModel: ObservableObject {
    @Published var trigger: Trigger
    @Published var inputs: [Input] = []

    init(trigger: Trigger) {
        self.trigger = trigger
        executeTrigger()
    }

    func executeTrigger() {
        // Execute the trigger logic and update CoreData accordingly
    }

    func createInputExecutions() {
        // Create InputExecution entities for each input of the trigger
    }
}
