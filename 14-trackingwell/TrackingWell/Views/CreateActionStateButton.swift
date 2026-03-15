//
//  CreateActionStateButton.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct CreateActionStateButton: View {
    @State private var isPresentingCreateView = false

    var body: some View {
        Button(action: {
            isPresentingCreateView = true
        }) {
            Text("Create Action State")
        }
        .sheet(isPresented: $isPresentingCreateView) {
            CreateEditActionStateView(viewModel: CreateEditActionStateViewModel())
        }
    }
}
