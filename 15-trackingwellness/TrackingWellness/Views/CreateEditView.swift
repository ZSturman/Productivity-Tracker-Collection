//
//  CreateEditView.swift
//  TrackingWellness
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct CreateEditView: View {
    @Environment(\.presentationMode) var presentationMode
    
    var actionState: ActionState?
    @StateObject var createEditVM: CreateEditVM

    init(actionState: ActionState?) {
        self.actionState = actionState
        _createEditVM = StateObject(wrappedValue: CreateEditVM(editActionState: actionState, actionStateVM: ActionStateVM(actionState: actionState ?? ActionState(title: ""))))
    }
    
    var body: some View {
        NavigationStack {
            
        }
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: {
                    presentationMode.wrappedValue.dismiss()
                }, label: {
                    Text("Save")
                })
            }
        }
    }
}
