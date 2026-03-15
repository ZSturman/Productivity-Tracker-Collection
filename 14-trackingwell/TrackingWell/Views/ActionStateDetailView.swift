//
//  ActionStateDetailView.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct ActionStateDetailView: View {
    @ObservedObject var viewModel: ActionStateDetailViewModel

    var body: some View {
        VStack {
            ExecutionList(viewModel: ExecutionListViewModel(actionState: viewModel.actionState))
            //TriggerButtonOne(trigger: viewModel.selectedTriggerOne)
            //TriggerButtonTwo(trigger: viewModel.selectedTriggerTwo)
            Spacer()
            Button("Edit", action: {
                // Handle edit action
            })
            Button("Delete", action: {
                // Handle delete action
            })
        }
    }
}
