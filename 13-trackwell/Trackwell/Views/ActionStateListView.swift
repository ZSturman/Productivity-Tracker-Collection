//
//  ActionStateListView.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/25/23.
//

import SwiftUI

struct ActionStateListView: View {
    @ObservedObject var vm: ActionStateListViewModel

    var body: some View {
        NavigationStack {
            if vm.actionStates.count == 0 {
                NoActionStateView()
            } else {
                List {
                    ForEach(vm.actionStates) { actionState in
                        ActionStateRowView(vm: ActionStateRowViewModel(actionState: actionState, actionStateListVM: vm))
                        // EXECUTION //
                            .swipeActions {
                                if actionState.triggers.contains(where: { $0.type == .SwipeLeftOne }) {
                                    Button(action: {
                                        vm.handleSwipeLeftOneAction(for: actionState)
                                    }) {
                                        Label("Button Three Action", systemImage: "arrow.right.circle.fill")
                                    }
                                    .tint(.blue)
                                }
                            }
                    }
                }
                .navigationTitle("Action States")
            }

        }
    }
}
