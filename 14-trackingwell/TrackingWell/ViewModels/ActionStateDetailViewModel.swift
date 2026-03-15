//
//  ActionStateDetailViewModel.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation

class ActionStateDetailViewModel: ObservableObject {
    @Published var actionState: ActionState

    init(actionState: ActionState) {
        self.actionState = actionState
        fetchActionStateDetails()
    }

    func fetchActionStateDetails() {
        // Fetch additional details for the given actionState if needed
    }
}
