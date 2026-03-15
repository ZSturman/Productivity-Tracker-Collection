//
//  ExecutionRow.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct ExecutionRow: View {
    var execution: Execution
    @ObservedObject var viewModel: ExecutionDetailViewModel

    var body: some View {
        NavigationLink(destination: ExecutionDetailView(viewModel: viewModel)) {
            Text("\(execution.timestamp ?? Date.now)")
        }
    }
}

