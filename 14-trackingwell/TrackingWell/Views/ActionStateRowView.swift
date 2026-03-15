//
//  ActionStateRowView.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct ActionStateRowView: View {
    var actionState: ActionState
    @ObservedObject var viewModel: ActionStateDetailViewModel

    var body: some View {
        NavigationLink(destination: ActionStateDetailView(viewModel: viewModel)) {
            VStack(alignment: .leading) {
                Text(actionState.title ?? "")
                    .font(.headline)
                Text(actionState.isAction ? "Action" : "State")
                    .font(.subheadline)
            }
        }
    }
}

