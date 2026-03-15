//
//  ExecutionDetailView.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct ExecutionDetailView: View {
    @ObservedObject var viewModel: ExecutionDetailViewModel

    var body: some View {
        VStack {
            Text(viewModel.executionDetailInfo)
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
