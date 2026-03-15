//
//  ActionStateDetailView.swift
//  TrackingWellness
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct ActionStateDetailView: View {
    @ObservedObject var actionState: ActionState
    @State private var showingSheet = false
    
    var body: some View {
        NavigationStack {
            
        }
        .navigationTitle(actionState.title)
        .toolbar{
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: {
                    showingSheet.toggle()
                }, label: {
                    Text("Edit")
                })
            }
        }
        .sheet(isPresented: $showingSheet) {
            CreateEditView(actionState: actionState)
        }
    }
}

