//
//  AddTriggerSheetView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import SwiftUI

struct AddTriggerSheetView: View {
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var vm: CreateActionStateVM
    
    var body: some View {
        NavigationStack {
            VStack {
                List {
                    ForEach(TriggerTypeOptions.allCases, id: \.rawValue) { triggerTypeOption in
                        Text(triggerTypeOption.triggerTypeName)
                            .opacity(self.isTriggerUsed(triggerType: triggerTypeOption) ? 0.5 : 1.0)
                            .onTapGesture {
                                if vm.addTriggerIfNotUsed(triggerType: triggerTypeOption) {
                                    dismiss()
                                }
                            }
                    }
                }
            }
            .navigationTitle("Add Trigger")
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
            }
        }
    }
    
    func isTriggerUsed(triggerType: TriggerTypeOptions) -> Bool {
        return vm.isTriggerUsed(triggerType: triggerType)

    }
}

struct AddTriggerSheetView_Previews: PreviewProvider {
    static var previews: some View {
        AddTriggerSheetView(vm: CreateActionStateVM(dataService: DataService()))
    }
}
