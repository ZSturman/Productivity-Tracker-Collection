//
//  ActionStateListViewModel.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/26/23.
//

import SwiftUI

class ActionStateListViewModel: ObservableObject {
    @Published var actionStates: [ActionState] = []
    
    func handleSwipeLeftOneAction(for actionState: ActionState) {
        print("Swipe Left One action triggered for \(actionState.title)")
    }


    // Logic to delete an action state
    func deleteActionState(at offsets: IndexSet) {
        actionStates.remove(atOffsets: offsets)
    }
}
